import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mne.io
from eeg_io import *

def plot_not_target(u_dat, epochs):
    return epochs["not-target"].average().plot()

def plot_basic_info(u_dat):
    return u_dat.plot(events = events,
                      event_color = {1: "green", 2: "blue", 3: "red"})

timing = pd.read_csv("../eeg_tests/timing.csv")


from mne.decoding import UnsupervisedSpatialFilter
from sklearn.decomposition import PCA, FastICA

from mne.preprocessing import ICA, create_ecg_epochs

# response is probably uninteresting as an "EVENT", rather, the stimuli should probably be classified as "got right" and "got wrong" so that the averaging captures evoked responses, and so we can capture induced responses, only on those stimuli that the user noticed! Otherwise we're just watering down caught signals with missed signals.



p25_dat, epochs, events = get_user_data('P25', timing)


X = epochs["target"].get_data()
ica = UnsupervisedSpatialFilter(FastICA(), average=False)
ica_data = ica.fit_transform(X)
ev1 = mne.EvokedArray(np.mean(ica_data, axis=0),
                      mne.create_info(32, epochs.info['sfreq'],ch_types='eeg'))

ev1.plot(show = False)

# filter out power-line noise
p25_dat.notch_filter(np.arange(50, 200, 50), filter_length='auto', phase='zero')

# band-pass 1-50 contains all the signal we like
p25_dat.filter(8, 13., h_trans_bandwidth='auto', filter_length='auto', phase = 'zero')

epochs = mne.Epochs(p25_dat, events, {"target": 1, "not-target": 2}, preload = True)

X = epochs["target"].get_data()
ica = UnsupervisedSpatialFilter(FastICA(), average=False)
ica_data = ica.fit_transform(X)
ev2 = mne.EvokedArray(np.mean(ica_data, axis=0),
                      mne.create_info(32, epochs.info['sfreq'],ch_types='eeg'))

ev2.plot(show = False)

# ICA

# explore difference in components based on "epoch", seems to be a split after
# epoch ~30, is this a different test? Group by
ica = ICA(n_components = .99, method='fastica')

ica.fit(epochs["target"]).plot_components(inst = epochs["target"])

ica.fit(epochs["not-target"]).plot_components(inst = epochs["not-target"])

from mne.io.pick import  _pick_data_channels
# look at target where user got correct answer vs not-target...
picks = _pick_data_channels(epochs.info, exclude='bads', with_ref_meg=False)
