from scipy.linalg import issymmetric,ishermitian
import numpy as np

matrix=np.array([[1,2,3],
                 [8,8,6],
                 [3,6,5]])

Matrix2= np.array([[2, 1j], 
              [-1j, 3]])
# if A and Transpose of A are same then it return True
print(issymmetric(matrix))
print(ishermitian(Matrix2))