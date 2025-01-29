import numpy as np

arr=np.array([[[1,2,3,4],
             [5,6,7,8],
             [9,10,11,12]]])
print(arr.shape) #output:(1,3,4) 

new_arr=np.array([1,2,3,4], ndmin=5)
print(new_arr.shape) #output:(1,1,1,1,4)