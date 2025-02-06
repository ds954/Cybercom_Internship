from scipy.linalg import eig_banded,eigvals_banded
import numpy as np

ab = np.array([[0,  0, -1, -1, -1],
               [0,  2,  2,  2,  2],
               [5,  4,  3,  2,  1],
               [1,  1,  1,  1,  0]])
eigan_values=eigvals_banded(ab)
print(eigan_values)
v=eig_banded(ab,eigvals_only=True,select='v',select_range=[-2,4])
# print(w)
print(v)