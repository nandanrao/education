from eeg_io import *
import pandas as pd


def calc_success(series, metric):
    if metric == 'precision':
        try:
            true_p, false_p = series[1], series[2]
            return true_p / (true_p + false_p)
        except KeyError:
            # 1 is the correct target, 2 is false target
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

def precision_df(df):
    predicted = df[df.code == 3]
    idx = predicted.index - 1

    # filter to only the non-repeat signals
    targets = df[(df.index.isin(idx) & (df.code != 3))]
    predicted = predicted[predicted.index.isin(targets.index + 1)]
    resp_times, target_times = predicted.timestamp.values, targets.timestamp.values
    times = (resp_times - target_times).astype(float)
    return targets.assign(response_time = times)

def n_back_response(df):
    return (precision_df(df)
            .groupby(['test', 'code'])
            .response_time
            .median()) # change to median???

def format_response_times(s):
    naming = lambda x: 'med_res_time_correct' if x == 1 else 'med_res_time_wrong'
    df = pd.DataFrame(s).reset_index()
    return (df
            .assign(code = df.code.map(naming))
            .rename(columns={'response_time': 'score', 'code': 'metric'}))

def n_back_precision(df):
    return (precision_df(df)
            .groupby(['test', 'code'])
            .count()
            .nothing)

def n_back_recall(df):
    positives = df[df.code == 1]
    idx = positives.index + 1
    predicted = df[(df.index.isin(idx) & (df.code == 3))]

    counts = (pd.concat([positives, predicted])
              .groupby(['test', 'code'])
              .count()
              .nothing)

    return counts

def n_back_get_scores(events):
    df = pd.DataFrame(events, columns = ['timestamp', 'nothing', 'code', 'test'])
    precision = success_by_targets(n_back_precision(df), 'precision').assign(metric = 'precision')
    recall = success_by_targets(n_back_recall(df), 'recall').assign(metric = 'recall')
    response_times = format_response_times(n_back_response(df))
    s = pd.concat([precision, recall, response_times])
    return s

def stroop_get_scores(user, timing):
    d = with_timing(user, timing)['stroop-summary']
    # metric = ('med_res_time_' +
    #           d.Task.str.replace(' ', '_').str.lower() +
    #           '_' +
    #           d.Congruency.str.lower())
    response_times = pd.DataFrame({'test': 'stroop',
                                   'metric': ['accuracy', 'med_res'],
                                   'score': [
                                       d.Accuracy.mean(),
                                       d['Median RT'].median()                                                                    ]})
    return response_times


def read_user_success(user, timing, eeg_data, targets):
    try:
        events = get_user_data(user, timing, eeg_data, targets, events_only = True)
        n_back = n_back_get_scores(events).assign(user = user)
        stroop = stroop_get_scores(user, timing).assign(user = user)
        df = pd.concat([n_back, stroop])
    except OSError as e:
        print('Could not find user: ', user, 'Error: ', e)
        df = pd.DataFrame([])
    return df

def read_all_user_success(timing, eeg_data, targets = ['three-back', 'two-back']):
    dfs = [read_user_success(u, timing, eeg_data, targets)
           for u in timing['File Prefix']]
    return pd.concat(dfs)
