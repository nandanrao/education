import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

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
