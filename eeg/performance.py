from eeg_io import *
import pandas as pd

def calc_success(series):
    yes, no = series.tolist()
    return yes / (yes + no)

def n_back_get_success(events):
    df = pd.DataFrame(events, columns = ['timestamp', 'nothing', 'code', 'test'])
    idx = df[df.code == 3].index - 1

    # QUESTION: how do we count if they press the button twice in a row?
    # currently we are just ignoring the subsequent presses.
    counts = (df[(df.index.isin(idx)) & (df.code != 3)]
              .groupby(['test', 'code'])
              .count()
              .nothing)
    targets = set([i[0] for i in counts.index])
    d = [(t, calc_success(counts[t])) for t in targets]
    return pd.DataFrame(d, columns = ['test', 'score'])

def read_user_success(user, timing, eeg_data, targets):
    try:
        events = get_user_data(user, timing, eeg_data, targets, events_only = True)
        df = n_back_get_success(events).assign(user = user)
    except OSError as e:
        print('Could not find user: ', user, 'Error: ', e)
        df = pd.DataFrame([])
    return df

def read_all_user_success(timing, eeg_data, targets = ['three-back', 'two-back']):
    dfs = [read_user_success(u, timing, eeg_data, targets)
           for u in timing['File Prefix']]
    return pd.concat(dfs)
