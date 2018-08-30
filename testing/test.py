import numpy as np
from functions.distance import klDist
from dtw import dtw
from dtw import fastdtw
import os
import time

def euc(x, y):
    # print('x : {0:s}'.format(str(x)))
    # print('y : {0:s}'.format(str(y)))
    # print()
    return np.sqrt(np.sum(np.square(x - y)))

def mat2list(mat):
    l = mat.shape[0]
    tmp = np.copy(mat)
    tmp = tmp.reshape((-1, 1))
    tmp = np.array_split(tmp, l)
    return tmp

os.system('clear')

A = np.random.rand(200, 9400)
B = np.random.rand(93, 9400)

start = time.time()
dist, cost, acc, path = dtw(mat2list(A), mat2list(B), klDist)
end = time.time()

print(dist)
# print(cost)
# print(acc)
# print(path)

print('{0:.2f} seconds'.format(end - start))

# a = np.random.rand(1, 5)
# b = np.random.rand(1, 5)
# print(klDist(a, b))