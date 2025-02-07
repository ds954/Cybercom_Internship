import numpy as np
from scipy.sparse import diags

def create_csr_matrix(diagonals, offsets, shape=(4, 4)):
    """
    Creates a sparse matrix in CSR (Compressed Sparse Row) format.
    """
    csr_matrix = diags(diagonals, offsets, shape=shape, format='csr')
    return csr_matrix

def create_csc_matrix(diagonals, offsets, shape=(4, 4)):
    """
    Creates a sparse matrix in CSC (Compressed Sparse Column) format.
    """
    csc_matrix = diags(diagonals, offsets, shape=shape, format='csc')
    return csc_matrix

def create_lil_matrix(diagonals, offsets, shape=(4, 4)):
    """
    Creates a sparse matrix in LIL (List of Lists) format.
    """
    lil_matrix = diags(diagonals, offsets, shape=shape, format='lil')
    return lil_matrix

def create_dia_matrix(diagonals, offsets, shape=(4, 4)):
    """
    Creates a sparse matrix in DIA (Diagonal) format.
    """
    dia_matrix = diags(diagonals, offsets, shape=shape, format='dia')
    return dia_matrix

def create_dok_matrix(diagonals, offsets, shape=(4, 4)):
    """
    Creates a sparse matrix in DOK (Dictionary of Keys) format.
    """
    dok_matrix = diags(diagonals, offsets, shape=shape, format='dok')
    return dok_matrix

# Define the diagonals and offsets for the sparse matrix
main_diag = np.array([1, 2, 3, 4])  # Main diagonal (offset 0)
upper_diag = np.array([5, 6, 7])    # Upper diagonal (offset 1)
lower_diag = np.array([8, 9, 10])   # Lower diagonal (offset -1)

# Sequence of diagonals
diagonals = [main_diag, upper_diag, lower_diag]

# Define the offsets corresponding to the diagonals
offsets = [0, 1, -1]

# Create matrices in different formats
csr_matrix = create_csr_matrix(diagonals, offsets)
# csc_matrix = create_csc_matrix(diagonals, offsets)
# lil_matrix = create_lil_matrix(diagonals, offsets)
# dia_matrix = create_dia_matrix(diagonals, offsets)
# dok_matrix = create_dok_matrix(diagonals, offsets)

# Print results
print("CSR Matrix:")
print(csr_matrix)
# print("\nCSC Matrix:")
# print(csc_matrix)
# print("\nLIL Matrix:")
# print(lil_matrix)
# print("\nDIA Matrix:")
# print(dia_matrix)
# print("\nDOK Matrix:")
# print(dok_matrix)

# Optionally convert them to dense arrays to visualize the result
print("\nDense CSR Matrix:")
print(csr_matrix.toarray())

# print("\nDense CSC Matrix:")
# print(csc_matrix.toarray())

# print("\nDense LIL Matrix:")
# print(lil_matrix.toarray())

# print("\nDense DIA Matrix:")
# print(dia_matrix.toarray())

# print("\nDense DOK Matrix:")
# print(dok_matrix.toarray())
