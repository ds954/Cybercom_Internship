import numpy as np

# Define two 1D arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Horizontally stack the 1D arrays
result_1D = np.hstack((arr1, arr2))
print("hstack with 1D arrays:\n", result_1D)
# Output: [1 2 3 4 5 6]

# Define two 2D arrays
arr3 = np.array([[1, 2, 3],
                 [4, 5, 6]])
arr4 = np.array([[7, 8, 9],
                 [10, 11, 12]])

# Horizontally stack the 2D arrays
result_2D = np.hstack((arr3, arr4))
print("hstack with 2D arrays:\n", result_2D)
# Output:
# [[ 1  2  3  7  8  9]
#  [ 4  5  6 10 11 12]]

# Define two 3D arrays
arr5 = np.array([[[1, 2], [3, 4]],
                 [[5, 6], [7, 8]]])
arr6 = np.array([[[9, 10], [11, 12]],
                 [[13, 14], [15, 16]]])

# Horizontally stack the 3D arrays (along axis 2)
result_3D = np.hstack((arr5, arr6))
print("hstack with 3D arrays:\n", result_3D)
# Output:
# [[[ 1  2  9 10]
#   [ 3  4 11 12]]
#
#  [[ 5  6 13 14]
#   [ 7  8 15 16]]]
