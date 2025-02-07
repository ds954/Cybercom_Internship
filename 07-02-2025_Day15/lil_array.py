import numpy as np
from scipy.sparse import lil_matrix

# Create a 4x5 LIL sparse matrix
lil = lil_matrix((4, 5), dtype=np.int32)

# Assign non-zero values to specific positions
lil[0, 0] = 1
lil[0, 3] = 3
lil[1, 2] = 5
lil[2, 1] = 7
lil[3, 4] = 9

# Print the sparse LIL matrix
print("LIL Matrix (sparse):")
print(lil)

# Convert the LIL matrix to a dense array and print
dense_array = lil.toarray()
print("\nLIL Matrix as Dense Array:")
print(dense_array)
