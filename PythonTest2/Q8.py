# Write a function transpose_matrix(matrix) that returns the transpose of a 2D matrix.
import numpy as np


def transpose_matrix(matrix):
    return matrix.T


matrix=np.array([[1,2,3],
                 [4,5,6]])
answer=transpose_matrix(matrix)
print(answer)

