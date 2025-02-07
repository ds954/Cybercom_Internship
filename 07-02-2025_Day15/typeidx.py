from scipy import sparse
import numpy as np
data = ['a','b','c']
indices = np.array([0, 1, 0])
indptr = np.array([0, 2, 3, 3])
A = sparse.csr_array((data, indices, indptr))
print(A.indptr.dtype)