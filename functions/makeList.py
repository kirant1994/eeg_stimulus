import numpy as np

def makeList(mat):
    l = mat.shape[0]
    tmp = np.copy(mat)
    tmp = tmp.reshape((-1, 1))
    tmp = np.array_split(tmp, l)
    return tmp