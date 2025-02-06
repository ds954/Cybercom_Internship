from scipy.linalg import eigh,eigvalsh
import numpy as np

arr=np.array([[1+5j,2,3],
              [4,5,6],
              [7,8,2+7j]])
value,vector=eigh(arr)
print(value)
print(vector)
eigenvalues=eigvalsh(arr)
print(eigenvalues)