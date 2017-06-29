import numpy as np
from itertools import permutations

# def score_rotation():
#     return True

# def match_cosines(A, B):
#     # for each a in A, find best B
#     print A.dot(B.T)
#     return A


def max_corr(A, B, axis=1):
    d1,d2 = A.shape[1], B.shape[1]
    cor = np.corrcoef(A, B, rowvar=False)[0:d1,d1:d1+d2]
    maxed = np.apply_along_axis(np.max, axis, cor)
    return np.abs(maxed)

def get_permutations(A, axis):
    """ Provides all permutations of an array along an axis, as list"""
    n = A.shape[axis]
    return [A[:,p] for p in permutations(range(n), n)]


def get_best_rotation(A, H, get_rotation, score):
    """ fn gets called with L = AT to return score to be maximized """
    A,H = np.array(A), np.array(H)
    perms = get_permutations(A, 1)
    Ts = [get_rotation(P, H) for P in perms]
    Ls = [A.dot(T) for T in Ts] # ONLY FOR ORTHOGONAL!
    scores = np.array([score(L) for L in Ls])
    i = np.argmax(scores)
    return perms[i], Ts[i]
