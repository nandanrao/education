import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from os import path
from sklearn.decomposition import SparsePCA
from sklearn.preprocessing import scale, normalize
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.linear_model import Lasso, ElasticNet
from scipy import stats
from bokeh.charts import Scatter

# do we still want this??
def viz_students(m, selected):
    d = pd.DataFrame(m, columns = ['one', 'two']).assign(user_id = ids, selected = selected)
    d.plot.scatter(x = 'one', y = 'two', c = 'selected')

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
    comps = np.matrix([(codes == i).astype(int) for i in codes.unique()]).T
    return normalize(comps, axis = 0)

def big_five_projection(bigfive, df, scaled = False):
    df = df if not scaled else df.apply(scale)
    comps = get_big_five_comps(bigfive)
    mat = df.as_matrix().dot(comps)
    bigfive_types = bigfive.bigfive_lbl_eng.unique()
    return pd.DataFrame(mat, columns = bigfive_types)

get_diff = lambda a,b: np.linalg.norm(a - b)/np.linalg.norm(a)

def compare_distance(d1, d2):
    a,b = [pairwise_distances(x, metric='mahalanobis') for x in [d1,d2]]
    return get_diff(a,b)

def test_distance_measure(metric, X = None, scaled = True):
    X = X if X is not None else (np.random.beta(1,10, 100) * 100).reshape(-1,1)
    a,b = (scale(X), scale(np.log(X))) if scaled else (X, np.log(X))
    d1 = pairwise_distances(a, metric = metric)
    d2 = pairwise_distances(b, metric = metric)
    return get_diff(d1, d2), get_diff(d2, d1)

distances = ['minkowski', 'seuclidean', 'sqeuclidean', 'euclidean', 'cosine', 'cityblock', 'chebyshev', 'canberra', 'braycurtis', 'mahalanobis']


def get_questions(comps, thresh = 0.01):
    comps = comps.T.tolist()
    a = pd.read_csv("educatalyst/Auxil/q3_key_teique.csv")
    b = pd.read_csv("educatalyst/Auxil/q4_key_grit.csv")
    questions = pd.concat([a,b], ignore_index=True).q_lbl_eng.tolist()
    return [pd.DataFrame([[n,q] for (n,q) in zip(c, questions) if abs(n) > thresh])
            for c in comps]


######################################################
# KENDALL TAU
def compare_order(m1, m2):
    cols = m1.shape[1]
    axes = [(m1[:,i], m2[:,i]) for i in range(cols)]
    return [stats.kendalltau(a,b) for a,b in axes]

def compare_factors(df1, comps1, df2, comps2):
    m1 = df1.dot(comps1).as_matrix()
    m2 = df2.dot(comps2).as_matrix()
    return compare_order(m1, m2)


######################################################
# Our regression classes
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

class MultiLasso(MultiElasticNet):
    def __init__(self, alpha=1.0, **kwargs):
        self.alpha = alpha
        self.l1_ratio = 1.0
        super(MultiLasso, self)
