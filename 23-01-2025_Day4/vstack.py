import numpy as np

# Define two 1D arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Vertically stack the 1D arrays
result_1D = np.vstack((arr1, arr2))
print("vstack with 1D arrays:\n", result_1D)
# Output:
# [[1 2 3]
#  [4 5 6]]
# Define two 2D arrays
arr3 = np.array([[1, 2, 3],
                 [4, 5, 6]])
arr4 = np.array([[7, 8, 9],
                 [10, 11, 12]])

# Vertically stack the 2D arrays
result_2D = np.vstack((arr3, arr4))
print("vstack with 2D arrays:\n", result_2D)
# Output:
# [[ 1  2  3]
#  [ 4  5  6]
#  [ 7  8  9]
#  [10 11 12]]

# Define two 3D arrays
arr5 = np.array([[[1, 2], [3, 4]],
                 [[5, 6], [7, 8]]])
arr6 = np.array([[[9, 10], [11, 12]],
                 [[13, 14], [15, 16]]])

# Vertically stack the 3D arrays (along axis 0)
result_3D = np.hstack((arr5, arr6))
print("vstack with 3D arrays:\n", result_3D)
result_3D = np.vstack((arr5, arr6))
print("vstack with 3D arrays:\n", result_3D)
# Output:
# [[[ 1  2]
#   [ 3  4]]
#
#  [[ 5  6]
#   [ 7  8]]]
#
#  [[[ 9 10]
#   [11 12]]
#
#  [[13 14]
#   [15 16]]]]
