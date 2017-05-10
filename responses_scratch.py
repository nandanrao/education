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
              for g in groups])

def prep_X(df):
    df = df.drop(['group', 'user_id'], 1)

    # Most are on a scale of 1-5, but the 300 questions are scaled
    # 1-7, so we just remove an extra 1 to center them.
    df -= 2.5
    df[list(df.filter(regex = '^3').columns)] -= 1
    return df

def big_five_projection(df):
    bigfive = pd.read_csv("educatalyst/Auxil/q1_key_bigfive.csv")
    codes = bigfive.bigfive_code
    df = df.filter(regex='^1')
    sums = [df.as_matrix().dot((codes == i).astype(int)) for i in codes.unique()]
    return np.matrix(sums).T

##############################################################
#
# Big Five explore
#
##############################################################
X = prep_X(read_surveys())

model = SparsePCA(5, .8).fit(X)
projected = model.transform(X)

dist_pre = scale(pairwise_distances(X, metric = "l2"))
dist_post = scale(pairwise_distances(projected, metric = "l2"))

fived = big_five_projection(X)
dist_five = scale(pairwise_distances(fived, metric = 'l2'))

np.linalg.norm(dist_post - dist_pre)
np.linalg.norm(dist_five - dist_pre)
np.linalg.norm(dist_five - dist_post)


# try with just 100
X = X.iloc[:, 0:65]
model = SparsePCA(5, .8).fit(X)
projected = model.transform(X)

dist_pre = scale(pairwise_distances(X, metric = "l2"))
dist_post = scale(pairwise_distances(projected, metric = "l2"))

np.linalg.norm(dist_post - dist_pre)
np.linalg.norm(dist_five - dist_pre)
np.linalg.norm(dist_five - dist_post)
##############################################################
#
# Surveys!!!!
#
##############################################################




pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q1.csv").head()

# Merge with big 5 and then run sparse PCA to see if we can find 5
# factors that describe the students???

# which do you most agree with, and how much with the other
# need to figure out how to likert encode this....
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q2.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_q2.csv").head()

# basic questions, likert scale...
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q3.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q4.csv").head()


# reformat this respondent/target and questions in columns
# 4 questions about (4/5?) peers, along the columsn, number after q's is peer.
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q5.csv").head(15)



# mates -- how many sides are the cube, it's between 6-20 >>> open ended.
# Purpose was to see them answer a range, nobody did, clearly a UI/question expectation
# problem...
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_mates.csv")
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_mates.csv")




pd.read_csv("educatalyst/Data/Raw/1606_jesuites_pilot/IJ_Prova_1_data.csv").head(20)
pd.read_csv("educatalyst/Data/Raw/1606_jesuites_pilot/IJ_Prova_1_data.csv").tail(20)
pd.read_csv("educatalyst/Data/Raw/1606_jesuites_pilot/IJ_Prova_1_data.csv").head()
