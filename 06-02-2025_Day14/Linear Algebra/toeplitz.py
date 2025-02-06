from scipy.linalg import solve_toeplitz,toeplitz
import numpy as np

#     [ 1 -1 -2 -3]       [1]
# T = [ 3  1 -1 -2]   b = [2]
#     [ 6  3  1 -1]       [2]
#     [10  6  3  1]       [5]

c = np.array([1, 3, 6, 10])    # First column of T
r = np.array([1, -1, -2, -3])  # First row of T
b = np.array([1, 2, 2, 5])
x = solve_toeplitz((c, r), b)
print(x)
T=toeplitz(c,r)
print(T.dot(x))