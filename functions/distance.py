import numpy as np
import sys

# def crossEntropy(p, q):
#     sum = 0
#     eps = sys.float_info.epsilon
#     if len(p) != len(q):
#         print('Vectors should be the same length for cross-entropy.')
#         return
#     for i in range(0, len(p)):
#         pi = p[i]
#         if q[i] == 0:
#             qi = q[i] + eps
#         else:
#             qi = q[i]
#         sum = sum - pi * np.log(qi)
#     return sum

def crossEntropy(p, q):
    eps = sys.float_info.epsilon
    return (-1 * np.sum(p * np.log(q + eps)))

# def klDist(true, sample):
#     return crossEntropy(true, sample) - crossEntropy(true, true)

def klDist(true, sample):
    eps = sys.float_info.epsilon
    return (-1 * np.sum(true * np.log(sample / (true + eps))))

def euclidean(true, sample):
    return np.sqrt(np.sum(np.square(true - sample)))
