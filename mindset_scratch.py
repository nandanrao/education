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
