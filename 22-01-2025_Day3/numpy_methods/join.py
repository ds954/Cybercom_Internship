import numpy as np

arr1 = np.array([[[1, 2], [3, 4],[10,11]]])
arr2 = np.array([[[5, 6], [7, 8],[15,16]]])

# Concatenate arr1 and arr2 along the columns (axis=1)
# This combines the arrays horizontally, keeping the rows intact
# arr = np.concatenate((arr1, arr2), axis=1)
# print("Concatenated array (axis=1):")
# print(arr)

# Stack arr1 and arr2 along the second axis (axis=1), effectively stacking them side by side as columns
# stack_arr = np.stack((arr1, arr2), axis=1)
# print("\nStacked array (axis=1):")
# print(stack_arr)

# Horizontally stack arr1 and arr2, combining them along axis=1
# This operation is similar to concatenate along axis=1
hstack_arr = np.hstack((arr1, arr2))
print(arr1)
print(arr2)
print("\nHorizontally stacked array (hstack):")

print(hstack_arr)

# Vertically stack arr1 and arr2, combining them along axis=0
# This will stack the arrays one on top of the other, preserving the columns
# vstack_arr = np.vstack((arr1, arr2))
# print("\nVertically stacked array (vstack):")
# print(vstack_arr)

# Stack arr1 and arr2 along the third axis (depth), effectively adding them as layers in a 3D array
# dstack_arr = np.dstack((arr1, arr2))
# print("\nDepth-wise stacked array (dstack):")
# print(dstack_arr)
