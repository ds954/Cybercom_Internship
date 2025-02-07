import numpy as np
from scipy.sparse import dia_matrix

# Define the non-zero values for the diagonals
data = np.array([[1, 2, 3],    # Main diagonal
                 [4, 5, 6],    # Diagonal above
                 [7, 8, 9]])   # Diagonal below

# Define the offsets for each diagonal (0: main, 1: above, -1: below)
offsets = np.array([0,1, -1])

# Create the DIA matrix
dia = dia_matrix((data, offsets), shape=(4,4))

# Print the DIA matrix (as sparse matrix)
print("DIA Matrix (sparse):")
print(dia)

# Convert the DIA matrix to a dense array
dense_array = dia.toarray()
print("\nDIA Matrix as Dense Array:")
print(dense_array)
