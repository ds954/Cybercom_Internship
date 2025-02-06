from scipy import linalg
import numpy as np

arr=np.array([[1,2],
              [4,5]])
inv_arr=linalg.inv(arr)
print(inv_arr)
print(np.dot(arr,inv_arr))