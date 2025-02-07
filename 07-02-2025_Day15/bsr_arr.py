import numpy as np
from scipy.sparse import bsr_matrix

# Block Sparse Row format sparse array.

row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 2])
data = np.array([1, 2, 3 ,4, 5, 6])

arr=np.array([[1, 0, 2],[0, 0, 3],[4, 5 ,6]])
print(bsr_matrix(arr))

bsr = bsr_matrix((data, (row, col)), shape=(3,3))

# Print the BSR matrix representation
print("BSR Matrix:")
print(bsr)

# Convert the BSR matrix to a dense array
dense_array = bsr.toarray()

# Print the dense representation of the matrix
print("BSR Matrix as Dense Array:")
print(dense_array)



