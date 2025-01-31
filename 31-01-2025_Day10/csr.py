import numpy as np
from scipy.sparse import csr_matrix

# Create a sparse matrix
data = np.array([1, 2, 0, 4, 5])  # Note the explicit zero
indices = np.array([0, 1, 2, 3, 4])
indptr = np.array([0, 2, 5])
A = csr_matrix((data, indices, indptr), shape=(2, 5))

print("Before eliminate_zeros():")
print(A)

A.eliminate_zeros()

print("\nAfter eliminate_zeros():")
print(A)
