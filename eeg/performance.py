from eeg.eeg_io import *
import pandas as pd
import re

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
    res = (precision_df(df)
            .groupby(['test'])
            .response_time
            .median()) 
    return pd.DataFrame({'test': res.index, 'score': res})

# def format_response_times(s):
#     return (df
#             .assign(code = df.code.map(naming))
#             .rename(columns={'response_time': 'score', 'code': 'metric'}))

def n_back_precision(df):
    return (precision_df(df)
            .groupby(['test', 'code'])
            .count()
            .nothing)

def get_recall_df(df):
    positives = df[df.code == 1]
    idx = positives.index + 1
    predicted = df[(df.index.isin(idx) & (df.code == 3))]    
    return positives, predicted

def n_back_recall(df):
    positives, predicted = get_recall_df(df)

    counts = (pd.concat([positives, predicted])
              .groupby(['test', 'code'])
              .count()
              .nothing)

    return counts

def get_clicks(df):
    a = df[df.code == 3].groupby(['test']).nothing.count()
    return pd.DataFrame({'test': a.index, 'score': a})


def transform_y(y, i):
    try:
        return 1 if y.iloc[i + 1] == 3 else 0
    except IndexError:
        return 0

def get_acc(df):
    idx = df[df.code != 3].index
    guesses = [transform_y(df.code, i) for i in idx]
    d = df[df.code != 3].assign(guess = guesses).assign(code = df.code.map(lambda x: 1 if x == 1 else 0))
    a = d.groupby('test').apply(lambda d: (d.code == d.guess).sum() / len(d) )
    return pd.DataFrame({ 'test': a.index, 'score': a})

def n_back_get_scores(events):
    df = pd.DataFrame(events, columns = ['timestamp', 'nothing', 'code', 'test'])
    precision = success_by_targets(n_back_precision(df), 'precision').assign(metric = 'precision')
    recall = success_by_targets(n_back_recall(df), 'recall').assign(metric = 'recall')
    response_times = n_back_response(df).assign(metric='med_res')
    clicks = get_clicks(df).assign(metric = 'clicks')
    accuracy = get_acc(df).assign(metric = 'accuracy')
    s = pd.concat([precision, recall, accuracy, response_times, clicks])
    return s

def stroop_get_scores(user, timing, pres):
    d = with_timing(user, timing, pres)['stroop-summary']
    # metric = ('med_res_time_' +
    #           d.Task.str.replace(' ', '_').str.lower() +
    #           '_' +
    #           d.Congruency.str.lower())
    response_times = pd.DataFrame({'test': 'stroop',
                                   'metric': ['accuracy', 'med_res'],
                                   'score': [d.Accuracy.mean(),
                                             d['Median RT'].median()]})
    return response_times


def read_user_success(user, timing, eeg_data, pres, targets):
    try:
        events = get_user_data(user, timing, eeg_data, pres, targets, events_only = True)
        n_back = n_back_get_scores(events).assign(user = user)
        stroop = stroop_get_scores(user, timing, pres).assign(user = user)
        df = pd.concat([n_back, stroop])
    except OSError as e:
        print('Could not find user: ', user, 'Error: ', e)
        df = pd.DataFrame([])
    return df

def read_all_user_success(timing, eeg_data, pres, targets = ['three-back', 'two-back']):
    dfs = [read_user_success(u, timing, eeg_data, pres, targets)
           for u in timing['File Prefix']]
    return pd.concat(dfs)

def design_perf_df(df):
    d = df.copy()
    d = (d
        .pivot_table(index=['user', 'test', 'metric'], values='score')
        .unstack(level=[1,2]))
    d.columns = ['_'.join(col).strip() for col in d.columns.values]
    d.index = [int(re.sub(r'[^\d]', '', s)) for s in d.index]
    d['treated'] = d.index > 23
    return d
