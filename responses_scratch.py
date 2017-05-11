import pandas as pd
import numpy as np


##############################################################
#
# Raw Data.
#
##############################################################


# which do you most agree with, and how much with the other
# need to figure out how to likert encode this....
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q2.csv").head()
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_q2.csv").head()

pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q3.csv").columns
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q4.csv").columns


# reformat this respondent/target and questions in columns
# 4 questions about (4/5?) peers, along the columsn, number after q's is peer.
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_q5.csv").head(15)



# mates -- how many sides are the cube, it's between 6-20 >>> open ended.
# Purpose was to see them answer a range, nobody did, clearly a UI/question expectation
# problem...
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/c_1612_mates.csv")
pd.read_csv("educatalyst/Data/Raw/1612_jesuites/ij_1612_mates.csv")
