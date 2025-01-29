import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print("Original array:")
print(arr)

#Using flatten() to create a new 1D array , return copy 
flattened_arr = arr.flatten()
print("\nArray using flatten():")
print(flattened_arr)
print("arr after flatten",arr)
flattened_arr[0]=25
print("after change value:")
print(flattened_arr)
print(arr)