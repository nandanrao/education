import numpy as np
from itertools import permutations
from sklearn.decomposition import FactorAnalysis
from factor_rotation._analytic_rotation import target_rotation
from factor_rotation._gpa_rotation import orthomax_objective, GPA
from sklearn.preprocessing import normalize
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
    """ fn gets called with L = AT to return score to be minimized"""
    A,H = np.array(A), np.array(H)
    perms = get_permutations(A, 1)
    Ts = [get_rotation(P, H) for P in perms]
    Ls = [A.dot(T) for T in Ts] # ONLY FOR ORTHOGONAL!
    scores = np.array([score(L) for L in Ls])
    i = np.argmin(scores)
    print "best rotation from permutation: " + str(i)
    return perms[i], Ts[i]

class RotatableFA(FactorAnalysis):
    def fit(self, X, y=None):
        super(RotatableFA, self).fit(X, y)
        self.trained_X_ = X
        return self

    def rotate_components(self, rotator, rotate_factors = False):
        """

        :param rotator: function that takes L, the loadings,
        and returns T in L* = LT, the rotation matrix applied to L
        :param include_factors: rotator takes a second argument
        which is the estimated factor matrix from the original training X.
        """
        if rotate_factors:
            F = self.transform(self.trained_X_)
            self.rotation_ = rotator(F)
        else:
            self.rotation_ = rotator(self.components_)
        self.components_ = self.components_.T.dot(self.rotation_).T
        return self

class VarimaxCorrelationObjective(object):
    """ Returns an objective function for optimizing varimax correlation matrix  """
    def __init__(self, Y, transpose = False):
        self.Y = Y
        self.transpose = transpose
        self.P = Y.shape[1]

    def varimax(self, A):
        return orthomax_objective(normalize(A), gamma=1, return_gradient=False)

    def __call__(self, A=None, T=None, L=None):
        L = A.dot(T) if L is None else L
        d1,d2 = self.P, self.P*2
        corr = np.corrcoef(L, self.Y, rowvar=False)[0:d1,d1:d2]
        if self.transpose:
            return self.varimax(corr.T)
        return self.varimax(corr)

class VarimaxGPA(object):
    def __init__(self, Y, transpose = False):
        self.Y = Y
        self.transpose = transpose

    def __call__(self, F):
        T = target_rotation(F, self.Y)
        ff = VarimaxCorrelationObjective(self.Y, self.transpose)
        _,_,T,_ = GPA(F, ff = ff, T = T)
        return T
