from eeg_io import *
import pandas as pd


def calc_success(series, metric):
    if metric == 'precision':
        try:
            true_p, false_p = series[1], series[2]
            return true_p / (true_p + false_p)
        except KeyError:
            return 1.0 if series.index[0] == 1 else 0.0

    if metric == 'recall':
        try:
            total, true_p = series[1], series[3]
            return true_p / total
        except KeyError:
            return 0.0

def success_by_targets(counts, metric):
    targets = set([i[0] for i in counts.index])
    d = [(t, calc_success(counts[t], metric)) for t in targets]
    return pd.DataFrame(d, columns = ['test', 'score'])

def n_back_precision(df):
    predicted = df[df.code == 3]
    idx = predicted.index - 1
    counts = (df[(df.index.isin(idx)) & (df.code != 3)]
              .groupby(['test', 'code'])
              .count()
              .nothing)

    return counts

def n_back_recall(df):
    positives = df[df.code == 1]
    idx = positives.index + 1
    predicted = df[(df.index.isin(idx) & (df.code == 3))]

    counts = (pd.concat([positives, predicted])
              .groupby(['test', 'code'])
              .count()
              .nothing)

    return counts

def n_back_get_scores(events, targets):
    df = pd.DataFrame(events, columns = ['timestamp', 'nothing', 'code', 'test'])
    precision = success_by_targets(n_back_precision(df), 'precision').assign(metric = 'precision')
    recall = success_by_targets(n_back_recall(df), 'recall').assign(metric = 'recall')

    s = pd.concat([precision, recall])
    return s

def read_user_success(user, timing, eeg_data, targets):
    try:
        events = get_user_data(user, timing, eeg_data, targets, events_only = True)
        df = n_back_get_scores(events, targets).assign(user = user)
    except OSError as e:
        print('Could not find user: ', user, 'Error: ', e)
        df = pd.DataFrame([])
    return df

def read_all_user_success(timing, eeg_data, targets = ['three-back', 'two-back']):
    dfs = [read_user_success(u, timing, eeg_data, targets)
           for u in timing['File Prefix']]
    return pd.concat(dfs)
