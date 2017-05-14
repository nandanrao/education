import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from os import path
from sklearn.decomposition import SparsePCA
from sklearn.preprocessing import scale
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.linear_model import Lasso, ElasticNet

def get_question_num(s, q):
    try:
        prefix = q * 100
        i = int(re.findall('->(\d+)', s)[0])
        return prefix + i if prefix else i
    except IndexError as e:
        lower = lambda x: x.lower()
        formatted = '_'.join(map(lower, s.split(' ')))
        return formatted if s == 'User Id' else formatted + '_' + str(q)

def read_df(group, q, folder = "educatalyst/Data/Raw/1612_jesuites"):
    f = group + '_1612_q' + str(q) + '.csv'
    p = path.join(folder, f)
    return (pd.read_csv(p)
            .drop(['End date', 'Start date', 'Duration'], 1) # Put these back?
            .rename(columns = lambda c: get_question_num(c, q)))

def read_surveys():
    qs = [1,3,4]
    groups = ['ij', 'c']
    return pd.concat([reduce(lambda a,b: pd.merge(a,b,on='user_id'),
                     [read_df(g, q) for q in qs]).assign(group = g)
              for g in groups], ignore_index = True)

def prep_X(df):
    df = df.drop(['group', 'user_id'], 1)

    on_seven_scale = list(df.filter(regex = '^3').columns)
    df[on_seven_scale] = df[on_seven_scale] * 5/7
    # Most are on a scale of 1-5, but the 300 questions are scaled
    # 1-7, so we just remove an extra 1 to center them.
    df -= 3

    return df

def get_big_five_comps(bigfive):
    codes = bigfive.bigfive_code
    return np.matrix([(codes == i).astype(int) for i in codes.unique()]).T

def big_five_projection(df):
    bigfive = pd.read_csv("educatalyst/Auxil/q1_key_bigfive.csv")
    df = df.filter(regex='^1')
    comps = get_big_five_comps(bigfive)
    return df.as_matrix().dot(comps)

class MultiLasso(Lasso):
    def __init__(self, alpha=1.0, **kwargs):
        # self.kwargs = kwargs
        # self.kwargs['alpha'] = alpha
        self.alpha = alpha

    def fit(self, X, Y):
        cols = Y.shape[1]
        r = range(cols)
        # print self.kwargs
        self.models = [Lasso(alpha = self.alpha).fit(X, Y[:,i]) for i in r]
        self.coef_ = [m.coef_ for m in self.models]
        self.original_var = [(np.asarray(Y[:,i] - Y[:,i].mean()) ** 2).sum() for i in r]


    def predict(self, X):
        if not self.models:
            raise Exception('bogus! No models???')
        return np.matrix([m.predict(X) for m in self.models]).T

    def scores(self, X, Y):
        if not self.models:
            raise Exception('bogus! No models???')
        r = range(Y.shape[1])
        return [self.models[i].score(X, Y[:,i]) for i in r]

    def score(self, X, Y):
        return np.mean(self.scores(X, Y))

class MultiElasticNet(ElasticNet):
    def __init__(self, alpha=1.0, l1_ratio = 0.5, **kwargs):
        self.alpha = alpha
        self.l1_ratio = l1_ratio

    def fit(self, X, Y):
        cols = Y.shape[1]
        r = range(cols)
        self.models = [ElasticNet(alpha = self.alpha, l1_ratio = self.l1_ratio)
                       .fit(X, Y[:,i]) for i in r]
        self.coef_ = [m.coef_ for m in self.models]
        self.original_var = [(np.asarray(Y[:,i] - Y[:,i].mean()) ** 2).sum() for i in r]
        return self

    def predict(self, X):
        if not self.models:
            raise Exception('bogus! No models???')
        return np.matrix([m.predict(X) for m in self.models]).T

    def scores(self, X, Y):
        if not self.models:
            raise Exception('bogus! No models???')
        r = range(Y.shape[1])
        return [self.models[i].score(X, Y[:,i]) for i in r]

    def score(self, X, Y):
        return np.mean(self.scores(X, Y))
