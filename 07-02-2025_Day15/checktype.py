import numpy as np
from scipy.sparse import  csr_matrix, issparse


print(issparse(csr_matrix([[5]])))
print(issparse(np.array([[5]])))
print(issparse(5))