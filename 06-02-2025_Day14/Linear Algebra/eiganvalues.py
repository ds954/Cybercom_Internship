from scipy.linalg import eigvals,eig
import numpy as np

# scalar values that indicate how much a vector stretches or shrinks
# det(A - λI) = 0 

arr=np.array([[5,4],
              [1,2]])
w,v=eig(arr)
print("eigen values:",w)
print("eigen vector:",v)
a,b=eigvals(arr)
print(a)
print(b)