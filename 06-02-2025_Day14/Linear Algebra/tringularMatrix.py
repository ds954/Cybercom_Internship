from scipy.linalg import solve_triangular
import numpy as np

a=np.array([[1,0,0,0],
            [2,3,0,0],
            [7,8,9,0],
            [5,2,3,7]])
b=np.array([7,8,9,10])
# ax=b
x=solve_triangular(a,b,lower=True)
print(x)
print(np.dot(a,x))