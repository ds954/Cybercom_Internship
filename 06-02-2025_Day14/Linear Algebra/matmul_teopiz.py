import numpy as np

from scipy.linalg import toeplitz, matmul_toeplitz
c = np.array([1, 3, 6, 10])    # First column of T
r = np.array([1, -1, -2, -3])  # First row of T
x = np.array([[1, 10], [2, 11], [2, 11], [5, 19]])
b=matmul_toeplitz((c, r), x)
print(b)
print(toeplitz(c, r))

# T x = b
#     [ 1 -1 -2 -3]       [1 10]
# T = [ 3  1 -1 -2]   x = [2 11]
#     [ 6  3  1 -1]       [2 11]
#     [10  6  3  1]       [5 19]