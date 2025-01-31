from scipy import linalg
import numpy as np

arr=np.array([[5,4],
              [1,2]])
a,b=linalg.eig(arr)
print(a)
print(b)