import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mne.io

from os import path, listdir
from fnmatch import fnmatch

dat = mne.io.read_raw_brainvision("EEG/P4 1215am 01312017.vhdr")

dat = mne.io.read_raw_brainvision("EEG/"+subject+" 900am 02062017.vhdr")


dat.load_data()
dat.drop_channels(["x_dir", "y_dir", "z_dir", "STI 014"])
dat.filter(1, 50)

montage = mne.channels.read_montage('biosemi32')

dat.set_montage(montage)

dat.plot()

plt.show()




survey = pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex1_graded.csv")


def read_pres_file(subject, ext, header, rm = None, sep = '\t', pres = "Presentation"):
    """ Reads all the files created by Presentation

    rm : str
    	Some of our log files repeat themselves, this filters the DF by column
    	in the string passed to remove the excess junk at the bottom.
    pres: str
    	Location of presentation folder
    """
    f = None
    for file in listdir(pres):
        if fnmatch(file, subject+ext):
            f = file
    if not f:
        raise Exception("could not find that file!")
    df = pd.read_csv(path.join(pres, f), sep=sep, header=header)
    return df[df[rm] == subject] if rm else df


def read_raw(subject):
    return { "two-back": read_pres_file(subject, "-2-Back.log", 2, "Subject"),
      "three-back": read_pres_file(subject, "-3-Back.log", 2, "Subject"),
      "stroop-log": read_pres_file(subject, "*Stroop Effect.log", 2, "Subject"),
      "stroop-text": read_pres_file(subject, "*Stroop Effect.txt", 0),
      "stroop-summary": read_pres_file(subject, "*Stroop Effect-Summary-*.txt", 0)
    }

# sometimes the 2-back and 3-back come at exactly the same time, sometimes slightly off

# what is stroop1full stroop1 practise etc., in the Stroop log and txt files I only have Main/Practise

# only P24 has 2-Stroop in the filename -- is this something different?
# what does "next" mean in the Time column??

# in all the log files, there's something weird where they start repeating some of the columns at the bottom of the file??

# Why does "subject" in stroop log suddenly turn from "P13" to "Picture"

# take times from video timing (excel), add the times from
