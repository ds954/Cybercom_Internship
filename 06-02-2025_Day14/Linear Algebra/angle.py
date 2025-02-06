import numpy as np
from scipy.linalg import subspace_angles,hadamard

# A Hadamard matrix is a square matrix where all entries are either +1 or -1, and most importantly, its columns (and rows) are mutually orthogonal, meaning any pair of columns (or rows) have a dot product of zero; essentially, they are perpendicular to each other in a geometric sense. 

A=np.array([[1,2,3],
            [4,5,6]])
B=np.array([[7,8,9],
            [4,5,6]])

# matrix=np.rad2deg(subspace_angles(A,B))
# print(matrix)
H = hadamard(4)
print(H)
result=np.rad2deg(subspace_angles(H[:, :2], H[:, 2:]))
print(result)