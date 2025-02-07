import numpy as np
from scipy.sparse import bsr_matrix
import scipy as sp
row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 2])
data = np.array([1, 2, 3 ,4, 5, 6])

bsr = bsr_matrix((data, (row, col)), shape=(3,3))
# sp.sparse.save_npz('bsr_matrix.npz',bsr)
sparse_arr=sp.sparse.load_npz('bsr_matrix.npz')
print(sparse_arr)
