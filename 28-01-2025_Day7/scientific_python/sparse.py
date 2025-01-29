import numpy as np
from scipy.sparse import csr_matrix

arr = np.array([[0, 0, 0], 
                [0, 0, 2], 
                [1, 0, 1]])

# Create a CSR (Compressed Sparse Row) matrix from the array
ans = csr_matrix(arr)

# Print the full sparse matrix representation
print("Sparse Matrix (CSR):")
print(ans)

# Print only the non-zero elements of the CSR matrix
print("\nNon-zero elements (data of CSR matrix):")
print(csr_matrix(arr).data)

# Print the count of non-zero elements in the CSR matrix
print("\nNumber of non-zero elements:")
print(csr_matrix(arr).count_nonzero())

# Eliminate zeros from the matrix (although no zeros in this case, this is for demonstration)
ans.eliminate_zeros()
print("\nSparse Matrix after eliminate_zeros (no change here):")
print(ans)

# Sum duplicates in the matrix (this combines duplicate values in each column)
ans.sum_duplicates()
print("\nSparse Matrix after sum_duplicates:")
print(ans)

# Convert the CSR matrix to CSC (Compressed Sparse Column) format
newarr = csr_matrix(arr).tocsc()

# Print the CSC matrix representation
print("\nCSC Matrix:")
print(newarr)
