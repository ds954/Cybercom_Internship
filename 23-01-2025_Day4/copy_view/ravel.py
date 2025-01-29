import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print("Original array:")
print(arr)
#Using ravel() to flatten the array  , return view
raveled_arr = arr.ravel()
print("\nArray using ravel():")
print(raveled_arr)
print("arr after ravel",arr)
raveled_arr[0]=25
print("after change value:")
print(raveled_arr)
print(arr)