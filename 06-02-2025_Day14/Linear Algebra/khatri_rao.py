import numpy as np
from scipy.linalg import khatri_rao

a = np.array([[1, 2, 3], 
              [4, 5, 6]])
b = np.array([[3, 4, 5], 
              [6, 7, 8], 
              [2, 3, 9]])
result=khatri_rao(a, b)
print(result)