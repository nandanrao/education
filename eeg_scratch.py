import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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

def read_pres_file(subject, ext, header, rm = None, sep = '\t', pres = "eeg_tests/logs"):
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
    # is this 10000/59.94??? no...
    adjusted_time =  df["Time"] + int((base_time - eeg_start) * 20)
    sample_num = adjusted_time / 20
    return df.assign(Time_Total = adjusted_time, sample_num = sample_num)

def with_timing(subject, timing):
    to_adjust = [("two-back", "2-Back Start"),
                 ("three-back", "3-Back Start")]
    logs = read_raw(subject)
    time = timing[timing["File Prefix"] == subject]
    for a in to_adjust:
        df = logs[a[0]]
        df["Time"] = pd.to_numeric(df["Time"])
        logs[a[0]] = adjust_timing(df, time[a[1]].values[0], time["EEG Start"].values[0])
    return logs

# two-back and three-back --> letter not important, picture_not_target, picture target, response
def encode_back_test(df):
    mapping = {"yes": 1, "no":2, np.nan: 3}
    return df["is_target(str)"].map(lambda x: mapping[x])

def make_event_df(df):
    return pd.DataFrame({"a": df.sample_num,
                         "b": np.zeros(len(df)),
                         "event_id": encode_back_test(df)})

def make_all_events(raw):
    targets = ["two-back", "three-back"]
    concat = lambda a,b: pd.concat([a,b])
    df = reduce(concat, map(lambda k: make_event_df(raw[k]), targets))
    return df.as_matrix().astype("int")

timing = pd.read_csv("eeg_tests/timing.csv")

p25 = with_timing("P25", timing)
p25_dat = load_eeg("P25")
events = make_all_events(p25)

# montage = mne.channels.read_montage('easycap-M10')
# p25_dat.set_montage(montage)
# mne.Epochs(p25_dat, events, {"two-back": 1}, -0.5)

p25_dat.plot(events = events, event_color = {1: "green", 2: "blue", 3: "red"})
plt.show()
