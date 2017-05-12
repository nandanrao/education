import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from os import path
from sklearn.decomposition import SparsePCA
from sklearn.preprocessing import scale
from sklearn.metrics.pairwise import pairwise_distances

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

    # Most are on a scale of 1-5, but the 300 questions are scaled
    # 1-7, so we just remove an extra 1 to center them.
    df -= 3
    df[list(df.filter(regex = '^3').columns)] -= 1
    return df

def big_five_projection(df):
    bigfive = pd.read_csv("educatalyst/Auxil/q1_key_bigfive.csv")
    codes = bigfive.bigfive_code
    df = df.filter(regex='^1')
    comps = np.matrix([(codes == i).astype(int) for i in codes.unique()])
    return df.as_matrix().dot(comps.T)
