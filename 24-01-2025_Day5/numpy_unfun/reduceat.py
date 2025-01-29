import numpy as np

# Example 1: Using np.outer (Outer product of two arrays)
a = np.array([1, 2, 3])
b = np.array([4, 5,6])

# The outer product of 'a' and 'b' results in a 2D matrix.
outer_result = np.outer(a, b)
print("Outer product (np.outer):\n", outer_result)
# np.outer does not change the original arrays a or b. It returns a new 2D array.

# Example 2: Using np.reduceat (Reduction over specific slices)
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
indices = [13, 7]

# np.reduceat reduces over specific slices of the array defined by 'indices'.
# It will apply a reduction (e.g., min) starting at each index in 'indices'.
reduce_result = np.minimum.reduceat(arr, indices)
print("\nReduction at specified indices (np.reduceat):\n", reduce_result)
# np.reduceat does not modify the original array. It returns a new array with reduced values.

# Example 3: Using np.at (Apply function element-wise at specific indices)
arr2 = np.array([1, 2, 3, 4, 5])

# np.add.at modifies the array in-place by adding 10 to the elements at the specified indices.
np.add.at(arr2, [0, 3], 10)  # Adds 10 to elements at indices 0 and 3
print("\nModified array after np.add.at:\n", arr2)
# np.at is an in-place operation, meaning it modifies the original array (arr2).

