import numpy as np
from scipy.linalg import eigvalsh_tridiagonal

# Define the diagonal elements
d = np.array([2, 3, 4])

# Define the off-diagonal elements (subdiagonal/superdiagonal)
e = np.array([1, 1])  # One element less than d

# Compute eigenvalues using SciPy
eigenvalues = eigvalsh_tridiagonal(d, e)

print("Eigenvalues:", eigenvalues)
