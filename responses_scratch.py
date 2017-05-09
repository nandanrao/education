import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from sklearn.decomposition import SparsePCA
from sklearn.preprocessing import scale
from sklearn.metrics.pairwise import pairwise_distances

def get_question_num(s):
    try:
        return int(re.findall('->(\d+)', s)[0])
    except:
        return s


##############################################################
#
# Big Five explore
#
##############################################################

bigfive = pd.read_csv("educatalyst/Auxil/q1_key_bigfive.csv")
xl_a = pd.read_excel("educatalyst/Data/Raw/1612_jesuites/Reports Educatalyst Educatalyst Casp (1).xlsx")
xl_b = pd.read_excel("educatalyst/Data/Raw/1612_jesuites/Reports Educatalyst Educatalyst Infant Jesus.xlsx")

#sns.distplot(xl_a[26]).show_one()
xl = (pd
      .concat([df.assign(source = src) for df,src in [(xl_a, "casp"), (xl_b, "infant")]])
      .rename(columns = get_question_num))

X = scale(xl.ix[:, 4:69])

model = SparsePCA(5, 0.8).fit(X)
projected = model.transform(X)

dist_pre = scale(pairwise_distances(X, metric = "l1"))
dist_post = scale(pairwise_distances(projected, metric = "l1"))



##############################################################
#
# Files, what these be???
#
##############################################################


# crazy formatting, sems needs to be Likert encoded
# which do you most agree with, and how much with the other
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q2.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_q2.csv").head()

# looks good, just like bigfive report
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q3.csv").head()

# looks good.
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q4.csv").head()

# 4 questions about (4/5?) peers, along the columsn, number after q's is peer.
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q5.csv").head(15)



pd.read_csv("educatalyst/Data/Raw/1606_jesuites_pilot/IJ_Prova_1_data.csv").head()


pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex1_graded.csv").head()
pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex1_graded.csv")["correct1"].unique()
pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex1_graded.csv")["correct1"].sum()


# these don't seem do have any grade...
pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex1_graded.csv")["correct2"].unique()
pd.read_csv("educatalyst/Data/Interim/ij_1612_coop_ex1_graded.csv")["correct1"].unique()
pd.read_csv("educatalyst/Data/Interim/ij_1612_coop_ex1_graded.csv")["correct2"].unique()


pd.read_csv("educatalyst/Data/Interim/ij_1612_coop_ex2_graded.csv").head()
pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex2_graded.csv").head()

# mates -- how many sides are the cube, it's between 6-20 >>> open ended.
