from scipy.linalg import solveh_banded
import numpy as np

ab = np.array([[ 4+0j,  5+0j,  6+0j,  7+0j, 8+0j, 9+0j],
               [ 2+1j,  2+1j,  2+1j,  2+1j, 2+1j, 0+0j],
               [-1-1j, -1-1j, -1-1j, -1-1j, 0+0j, 0+0j]])

# Complex right-hand side vector
b = np.array([1+2j, 2-1j, 2+0j, 3+1j, 3-2j, 3+0j])
x = solveh_banded(ab, b, lower=True)
print(x)
