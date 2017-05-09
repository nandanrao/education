import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

########################################################################
#
# MINDSET
#
# Count the number of tiles outside of some other number of tiles. There's a formula
# see if they get better.
# Really the only measurement we care about here is some latent variable of learning,
# we have no way to learn it supervised, so it will almost be a hand-crafted formula
# something like: Did poorly, then did well. Features needed for this:
# 1) success/fail on each round
# 2) watched video on each round
# 3) improved after watching video? Or improved after failing?
# The question will really be, see if we can create some structure, then we can also
# try and match it to survey questions and "known" psychological traits.

# around a couple tiles
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg1.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_preg1.csv").head()

#around 7 tiles
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg2.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_preg2.csv").head()

# around 30 tiles
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg3.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_preg3.csv").head()

# can you write the formula that would hold for any files - preg4mod is graded!
# how long are the videos!
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg4.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_preg4.csv").head()

pd.read_csv("educatalyst/Data/Interim/ij_1612_preg4_mod.csv").head(20)
pd.read_csv("educatalyst/Data/Interim/c_1612_preg4_mod.csv").head(20)


def make_df(df, num):
    n = str(num)
    return pd.DataFrame({
        'id': df['User Id'],
        'grade_'+n: df['Grade'],
        'duration_'+n: df['Duration']
    })

def get_4(group):
    df = pd.read_csv('educatalyst/Data/Interim/'+group+'_1612_preg4_mod.csv')
    grade = df.iloc[:, 5:8].dot(np.array([1,0.5,0.05]))
    return df.assign(Grade = grade)

def read_group(g, folder = 'educatalyst/Data/Raw/1612_jesuites'):
    nums = [1,2,3]
    make_file = lambda g,n: g + '_1612_preg' + str(n) + '.csv'
    dfs = [pd.read_csv(os.path.join(folder,  make_file(g, n)))
            for n in nums]

    # special shit for 4 which is weird:
    dfs.append(get_4(g))
    nums.append(4)

    # select the cols we want and combine
    dfs = [make_df(d, n) for d,n in zip(dfs, nums)]
    return reduce(lambda a,b: pd.merge(a,b, on='id'), dfs)

def read_dfs():
    groups = ['c', 'ij']
    return pd.concat([read_group(g) for g in groups], ignore_index = True)


from sklearn.decomposition import PCA

import matplotlib
def show_one(self):
    fig = self.get_figure()
    fig.savefig("/tmp/chart.png", dpi=90)
    fig.clear()

# def show_(self):
#     self.savefig("/tmp/chart.png", dpi=90)
#     self.clear()

matplotlib.artist.Artist.show_one = show_one
# matplotlib.pyplot.show_ = show_


df = read_dfs()
f = df.dropna().drop('id', 1)

sns.distplot(df.duration_1.dropna()).show_one()

sns.distplot(df.duration_2).show_one()

sns.distplot(df.duration_3).show_one()


# this is really the most interesting group (grade_1 adds nothing)
df[df.grade_4 == 1.0][(df.grade_3 < 1.0) | (df.grade_2 < 1.0) | (df.grade_1 < 1.0)]


# label based on when improved and plot their times on the distplot of all times
# for that round... or against those who deproved that round
improved_2 = (df.grade_4 == 1.0) & ((df.grade_3 < 1.0) | (df.grade_2 < 1.0) | (df.grade_1 < 1.0)) & (df.grade_3 > df.grade_2)

deproved_2 = ((df.grade_3 < 1.0) | (df.grade_2 < 1.0) | (df.grade_1 < 1.0)) & (df.grade_2 > df.grade_3)

improved_3 = (df.grade_4 == 1.0) & ((df.grade_3 < 1.0) | (df.grade_2 < 1.0) | (df.grade_1 < 1.0)) & (df.grade_4 > df.grade_3)

sns.distplot(df[improved_2].duration_2).plot(label = 'improved')
sns.distplot(df[deproved_2].duration_2).plot(label = 'deproved')
plt.show()
