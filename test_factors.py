import numpy as np
from factors import *
from scipy.spatial.distance import cosine, pdist, squareform
from factor_rotation._gpa_rotation import GPA
from factor_rotation._analytic_rotation import target_rotation

# def test_match_cosines():
#     A = np.array([[0,1,0], [1,0,0]])
#     B = np.array([[0,.2,.5], [.5,0,0]])
#     matched = match_cosines(A, B)
#     assert(matched[0] == (np.array([0,1,0], np.array([0,0,.5]))))

def test_max_corr_if_same():
    a = np.random.normal(size = (10,5))
    assert max_corr(a, a).sum() == 5.0

def test_get_permutations():
    A = np.random.normal(size = (2,5))
    perms = get_permutations(A, 1)
    assert len(perms) == 120
    assert np.all(perms[0] == A) # First permutation is the o.g. array!

def test_get_best_rotation_works_when_needs_to_flip_columns():
    # TODO: Come up with a test case for this!!!
    a = np.array([[0.01, 1.0], [1.0, 0.01]])
    b = np.array([[1.0,0.01], [0.01, 1.0]])
    fn = lambda A: max_corr(a, b).sum()
    P,T = get_best_rotation(a, b, target_rotation, fn)
    assert np.all(P == a) == True
