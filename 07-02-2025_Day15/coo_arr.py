import numpy as np
from scipy.sparse import coo_matrix,bsr_matrix
#  COOrdinate format
# Define the non-zero elements of the sparse matrix
data = np.array([4, 5, 7, 9])

# Define the row indices for these elements
row = np.array([0, 1, 2, 3])

# Define the column indices for these elements
col = np.array([1, 2, 3, 0])

# Create a COO sparse matrix with the specified data, row, and column indices
sparse_matrix = coo_matrix((data, (row, col)), shape=(4, 4))

print("COO Sparse Matrix:")
print(sparse_matrix)

# Convert the COO sparse matrix to a dense matrix and print it
dense_matrix = sparse_matrix.toarray()
print("\nDense Matrix:")
print(dense_matrix)
