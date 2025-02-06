import numpy as np
from scipy.linalg import solve_banded
ab = np.array([[0,  0, -1, -1, -1],
               [0,  2,  2,  2,  2],
               [5,  4,  3,  2,  1],
               [1,  1,  1,  1,  0]])
# a type of  matrix where non-zero elements are only present within a diagonal band around the main diagonal
# ax = b
#     [5  2 -1  0  0]       [0]
#     [1  4  2 -1  0]       [1]
# a = [0  1  3  2 -1]   b = [2]
#     [0  0  1  2  2]       [2]
#     [0  0  0  1  1]       [3]
b = np.array([0, 1, 2, 2, 3])
x = solve_banded((1, 2), ab, b)
print(x)