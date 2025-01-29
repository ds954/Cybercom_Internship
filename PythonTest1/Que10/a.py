# Convert the following 1D array into a 2×3 matrix:
# arr = np.array([1, 2, 3, 4, 5, 6])
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6])
reshaped_arr=arr.reshape(2,3)
print(reshaped_arr.shape)
print(reshaped_arr)