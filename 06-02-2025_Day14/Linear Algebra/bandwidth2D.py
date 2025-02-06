from scipy.linalg import bandwidth
import numpy as np

arr=np.array([[1,2,0,0,0],
              [7,8,9,0,0],
              [5,4,2,3,0],
              [1,7,5,3,6],
              [0,2,1,3,5]])
print(bandwidth(arr)) #Lower and Upper Bandwidth 