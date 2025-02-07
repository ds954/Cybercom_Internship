import numpy as np
from scipy.ndimage import convolve

# Input array
arr = np.array([[1, 2, 3, 4],
                [5, 7, 8, 9],
                [10, 20, 30, 40],
                [2,7,9,4]])

# Kernel
k = np.array([[-1, -1, 1],
              [0, 1, 0],
              [1, 0, 1]])

# [1 0 1]
# [0 1 0]
# [1 -1 -1]
# n+2p-f+1
# Padding the array with constant value (1.0) on all sides
padded_arr = np.pad(arr, pad_width=1, mode='wrap')

# Show the padded array
print("Padded array:")
print(padded_arr)

# Perform convolution
img = convolve(arr, k, mode='wrap')

# Show the result of the convolution
print("\nConvolved image:")
print(img)
