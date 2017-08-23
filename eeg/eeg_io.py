import pandas as pd
import numpy as np
import mne.io
from os import path, listdir
from fnmatch import fnmatch


def load_eeg(subject, directory = "EEG"):
    """ Load EEG data, filter 1-50Hz, drops useless channels """
    dat = mne.io.read_raw_brainvision(get_file(directory, subject+"*.vhdr"), scale= 0.01)
    dat.load_data()
    dat.drop_channels(["x_dir", "y_dir", "z_dir", "STI 014"])
    dat.filter(1, 50)
    dat, _ = mne.set_eeg_reference(dat, [])
    return dat

def get_file(directory, pat):
    """ Gets file from unix pattern blob """
    for file in listdir(directory):
        if fnmatch(file, pat):
            return path.join(directory, file)

def read_pres_file(subject, ext, header, rm = None, sep = '\t', pres = "../eeg_tests/logs"):
    """ Reads all the files created by Presentation

    rm : str
    	Some of our log files repeat themselves, this filters the DF by column
    	in the string passed to remove the excess junk at the bottom.
    pres: str
    	Location of presentation folder
    """
    f = get_file(pres, subject+ext)
    if not f:
        raise Exception("could not find that file!")
    df = pd.read_csv(f, sep=sep, header=header)
    return df[df[rm] == subject] if rm else df

def read_raw(subject):
    return { "two-back": read_pres_file(subject, "-2-Back.log", 2, "Subject"),
      "three-back": read_pres_file(subject, "-3-Back.log", 2, "Subject"),
      "stroop-log": read_pres_file(subject, "*Stroop Effect.log", 2, "Subject"),
      "stroop-text": read_pres_file(subject, "*Stroop Effect.txt", 0),
      "stroop-summary": read_pres_file(subject, "*Stroop Effect-Summary-*.txt", 0)
    }

def adjust_timing(df, base_time, eeg_start):
    # adjust for whatever takes this excel timing sheet into 1/10ths of ms
    adjusted_time =  df["Time"] + int((base_time - eeg_start) * 20)
    sample_num = adjusted_time / 20
    return df.assign(Time_Total = adjusted_time, sample_num = sample_num)

def with_timing(subject, timing):
    to_adjust = [("two-back", "2-Back Start"),
                 ("three-back", "3-Back Start"),
                 ("stroop-log", "Stroop1 Practice")]
    logs = read_raw(subject)
    time = timing[timing["File Prefix"] == subject]
    for a in to_adjust:
        df = logs[a[0]]
        df["Time"] = pd.to_numeric(df["Time"])
        logs[a[0]] = adjust_timing(df, time[a[1]].values[0], time["EEG Start"].values[0])
    return logs

# two-back and three-back --> letter not important, picture_not_target, picture target, response
def encode_test(df):
    try:
        # N-Back test
        mapping = {"yes": 1, "no":2, np.nan: 3}
        series = df['is_target(str)']
    except KeyError:
        # Stroop test -- drop Practice??? Included now...
        mapping = {"Incongruent": 1, "Neutral":2 }
        series = df['trial_cond(str)'].dropna()
        print series.size
    return series.map(lambda x: mapping[x])

def make_event_df(df):
    return pd.DataFrame({"a": df.sample_num,
                         "b": np.zeros(len(df)),
                         "event_id": encode_test(df)})

def make_all_events(raw, targets):
    concat = lambda a,b: pd.concat([a,b])
    df = reduce(concat, map(lambda k: make_event_df(raw[k]), targets))
    print df.size
    return df.as_matrix().astype("int")

def set_montage(u_dat):
    montage = mne.channels.read_montage('easycap-M10')
    u_dat.set_montage(montage)
    return u_dat

def get_user_data(user, timing, tmin = -.2, tmax = .7, l_freq = 1., h_freq = 50., targets = ["two-back", "three-back"]):
    u = with_timing(user, timing)
    u_dat = set_montage(load_eeg(user, "../data/EEG"))
    u_dat.filter(l_freq, h_freq, h_trans_bandwidth='auto', filter_length='auto', phase = 'zero')
    events = make_all_events(u, targets)
    encoding = {"target": 1, "not-target": 2}
    epochs = mne.Epochs(u_dat, events, encoding, tmin, tmax, preload = True)
    return u_dat, epochs, events
