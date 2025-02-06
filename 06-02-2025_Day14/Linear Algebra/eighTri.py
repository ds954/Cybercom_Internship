import numpy as np
from scipy.linalg import eigh_tridiagonal

# Define the diagonal elements
d = np.array([2, 3, 4])

# Define the off-diagonal elements
e = np.array([1, 1])

# Compute eigenvalues and eigenvectors
eigenvalues, eigenvectors = eigh_tridiagonal(d, e, eigvals_only=False)

print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)
