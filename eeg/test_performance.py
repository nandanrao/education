from performance import *
import pandas as pd

def test_calc_success_computes_precision_and_recall():
    assert calc_success(pd.Series([15,5], index=[1,2]), 'precision') == 3/4
    assert calc_success(pd.Series([15,5], index=[1,3]), 'recall') == 1/3

def test_calc_success_handles_missing_datal():
    assert calc_success(pd.Series([15], index=[1]), 'recall') == 0.0
    assert calc_success(pd.Series([15], index=[2]), 'precision') == 0.0
    assert calc_success(pd.Series([15], index=[1]), 'precision') == 1.0

# def test_n_back_precision_with_times():
#     df = pd.DataFrame([[1000, 0, 1, 'foo'], [1200, 0, 3, 'foo']],
#                       columns = ['timestamp', 'nothing', 'code', 'test'])
