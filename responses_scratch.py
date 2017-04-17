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


# coopex.csv ALMOST == coop_ex1.csv ????
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_coopex.csv") == pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_coop_ex1.csv")

pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_coop1.csv")

pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_coop_ex1.csv")

# crazy formatting, sems needs to be Likert encoded
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q2.csv").head()

# i can't see a difference with this ij "interim" file...
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_q2.csv").head()

# looks good, just like bigfive report
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q3.csv").head()

# looks good.
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q4.csv").head()

# looks ok, just need to create a separate key for Auxil
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q5.csv").head()

# Have no idea what these Q01 and such refer to!!!
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q6.csv").head()


pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_coop_ex1.csv").tail(20)

# these don't seem do have any grade...
pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex1_graded.csv")["correct1"].unique()
pd.read_csv("educatalyst/Data/Interim/ij_1612_coop_ex1_graded.csv")["correct1"].unique()
pd.read_csv("educatalyst/Data/Interim/ij_1612_coop_ex1_graded.csv")["correct2"].unique()

# these don't look the same!
pd.read_csv("educatalyst/Data/Interim/ij_1612_coop_ex2_graded.csv")["correct1"]
pd.read_csv("educatalyst/Data/Interim/c_1612_coop_ex2_graded.csv")["correct1"]

# No idea what this is, but it's graded!
pd.read_excel("educatalyst/Data/Interim/c_1612_mindset1.xlsx").head()

# the mod seems to be graded and usable
pd.read_excel("educatalyst/Data/Interim/c_1612_preg4.xlsx").head()
pd.read_csv("educatalyst/Data/Interim/c_1612_preg4_mod.csv").head()


# no idea what these are. More tests!
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg1.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg2.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg3.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_preg4.csv").head(20)


pd.read_csv("educatalyst/Data/Raw/1606_jesuites_pilot/IJ_Prova_1_data.csv").head(20)
pd.read_csv("educatalyst/Data/Raw/1606_jesuites_pilot/IJ_Prova_1_data.csv").tail(20)
