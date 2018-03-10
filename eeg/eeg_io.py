import pandas as pd
import numpy as np
import mne.io
from os import path, listdir
from fnmatch import fnmatch
from functools import reduce

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
        raise OSError("could not find that file!")
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
    for test,col in to_adjust:
        df = logs[test]
        df["Time"] = pd.to_numeric(df["Time"])
        try:
            logs[test] = adjust_timing(df, time[col].values[0], time["EEG Start"].values[0])
        except ValueError as e:
            print('ValueError while adjusting timing: ', e, 'This test will be lost: ', test, 'From user: ', subject)
            logs[test] = None
    return logs

# two-back and three-back --> letter not important, picture_not_target, picture target, response
def encode_test(df):
    try:
        # N-Back test
        mapping = {"yes": 1, "no":2, np.nan: 3}
        series = df['is_target(str)']
    except KeyError:
        # Stroop test -- drop Practice??? Included now...
        df[df.block == 'Main']
        # ink, color name, hit, miss... for stroop_text or log?
        mapping = {"Incongruent": 1, "Neutral":2 }
        series = df['trial_cond(str)'].dropna()
    return series.map(lambda x: mapping[x])

def make_event_df(df, k):
    if df is None:
        return pd.DataFrame([])
    return pd.DataFrame({"a": df.sample_num,
                         "b": np.zeros(len(df)),
                         "event_id": encode_test(df),
                         "target": k})

def make_all_events(raw, targets):
    concat = lambda a,b: pd.concat([a,b])
    df = reduce(concat, map(lambda k: make_event_df(raw[k], k), targets))
    return df.as_matrix()

def set_montage(u_dat):
    montage = mne.channels.read_montage('easycap-M10')
    u_dat.set_montage(montage)
    return u_dat

def get_user_data(user, timing,  eeg_data_folder, tmin = -.2, tmax = .7, l_freq = 1., h_freq = 50., targets = ["two-back", "three-back"], events_only = False):
    u = with_timing(user, timing)
    events = make_all_events(u, targets)
    if events_only:
        return events

    # For calculating epochs we need events as numpy in array
    # drop column "target" with test type
    events = events[:,:3].astype("int")
    u_dat = set_montage(load_eeg(user, eeg_data_folder))
    u_dat.filter(l_freq, h_freq, h_trans_bandwidth='auto', filter_length='auto', phase = 'zero')
    u_dat.notch_filter([50], filter_length = 'auto', phase = 'zero')
    encoding = {"target": 1, "not-target": 2}
    epochs = mne.Epochs(u_dat, events, encoding, tmin, tmax, preload = True)
    return u_dat, epochs, events
