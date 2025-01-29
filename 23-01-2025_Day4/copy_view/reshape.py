import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print("Original array:")
print(arr)

# 1. Using reshape(-1) to flatten the array , return view
reshaped_arr = arr.reshape(-1)
print("\nArray using reshape(-1):")
print(reshaped_arr)
reshaped_arr[0]=25
print("after change reshaped array:",reshaped_arr)
print("arr after reshape",arr)