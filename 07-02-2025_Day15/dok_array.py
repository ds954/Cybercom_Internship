import numpy as np
from scipy.sparse import dok_matrix
import scipy as sp

# Create a 4x4 sparse matrix in DOK format
# Initially empty, no non-zero elements
dok = dok_matrix((4, 4))

# Insert values into the DOK matrix (row, column) : value
dok[0, 1] = 1
dok[1, 2] = 2
dok[2, 3] = 7
dok[3, 0] = 4



# Print the DOK matrix (as sparse matrix)
print("DOK Matrix (sparse):")
print(dok)

# Convert the DOK matrix to a dense array
dense_array = dok.toarray()
print("\nDOK Matrix as Dense Array:")
print(dense_array)
print(dok.tocsr().toarray())