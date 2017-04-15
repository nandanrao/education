import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mne.io
from os import path, listdir
from fnmatch import fnmatch

def load_eeg(subject, directory = "EEG"):
    """ Load EEG data, filter 1-50Hz, drops useless channels """
    dat = mne.io.read_raw_brainvision(get_file(directory, subject+"*.vhdr"))
    dat.load_data()
    dat.drop_channels(["x_dir", "y_dir", "z_dir", "STI 014"])
    dat.filter(1, 50)
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

def adjust_timing(df, base_time):
    # I think the base_time is in ms, not 1/10ths ms.
    adjusted_time =  df["Time"].add(int(base_time * 10))
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
        logs[a[0]] = adjust_timing(df, time[a[1]].values[0])
    return logs



# montage = mne.channels.read_montage('biosemi32')
# dat.set_montage(montage)

timing = pd.read_csv("eeg_tests/timing.csv")
p25 = with_timing("P25", timing)
p25_dat = load_eeg("P25")

# convert the events from the actual two-back frame into num-coded events!
# concat with three-back, etc.
events = pd.DataFrame({"a": p25["two-back"].sample_num, "b": np.zeros(len(p25["two-back"])), "event_id": np.ones(len(p25["two-back"]))}).as_matrix().astype("int")

# mne.Epochs(p25_dat, events, {"two-back": 1}, -0.5)

p25_dat.plot(events = events)
plt.show()



# sometimes the 2-back and 3-back come at exactly the same time, sometimes slightly off

# what is stroop1full stroop1 practise etc., in the Stroop log and txt files I only have Main/Practise

# only P24 has 2-Stroop in the filename -- is this something different?
# what does "next" mean in the Time column??

# I assume that the "timing" excel sheet from Video is in milliseconds, not 1/10 milliseconds?

# in all the log files, there's something weird where they start repeating some of the columns at the bottom of the file??

# Why does "subject" in stroop log suddenly turn from "P13" to "Picture"

# take times from video timing (excel), add the times from
