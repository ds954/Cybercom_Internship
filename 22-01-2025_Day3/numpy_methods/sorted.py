import numpy as np

arr = np.array([1,2, 3,4, 5,6,7,8,9])

# `np.searchsorted()` returns the index of where a value (or list of values) should be inserted to maintain order.
# Using side='right' means it will return the index of the first element that is greater than or equal to the search value.
result = np.searchsorted(arr, 4,side='right')
# 4 should be inserted at index 2 to keep the array sorted.
print(result)  # Output: 2

# Searching for multiple values at once using np.searchsorted
newarr = np.searchsorted(arr, [2, 4, 6],side='right')
# 2 should be inserted at index 1, 4 at index 2, and 6 at index 3.
print(newarr)  # Output: [1 2 3]
