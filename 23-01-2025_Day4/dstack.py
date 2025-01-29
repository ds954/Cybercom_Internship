import numpy as np

# Define two 1D arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Stack the 1D arrays along the third dimension
result_1D = np.dstack((arr1, arr2))
print("dstack with 1D arrays:\n", result_1D)
# Output:
# [[[1 4]
#   [2 5]
#   [3 6]]]

# Define two 2D arrays
arr3 = np.array([[1, 2, 3],
                 [4, 5, 6]])
arr4 = np.array([[7, 8, 9],
                 [10, 11, 12]])

# Stack the 2D arrays along the third dimension (depth)
result_2D = np.dstack((arr3, arr4))
print("dstack with 2D arrays:\n", result_2D)
# Output:
# [[[ 1  7]
#   [ 2  8]
#   [ 3  9]]
#
#  [[ 4 10]
#   [ 5 11]
#   [ 6 12]]]

# Define two 3D arrays
arr5 = np.array([[[1, 2], [3, 4]],
                 [[5, 6], [7, 8]]])
arr6 = np.array([[[9, 10], [11, 12]],
                 [[13, 14], [15, 16]]])

# Stack the 3D arrays along the third dimension (depth-wise)
result_3D = np.dstack((arr5, arr6))
print("dstack with 3D arrays:\n", result_3D)
# Output:
# [[[ 1  9]
#   [ 2 10]]
#
#  [[ 3 11]
#   [ 4 12]]]
#
#  [[[ 5 13]
#   [ 6 14]]
#
#  [[ 7 15]
#   [ 8 16]]]]
