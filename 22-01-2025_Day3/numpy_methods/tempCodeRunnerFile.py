import numpy as np

arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
splitted_arr=np.array_split(arr,3)#If the array has less elements than required, it will adjust from the end accordingly.
print("split array along row:")
print(splitted_arr)

#2D array with 6 rows and 3 columns
newarr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])

hsplitted_arr = np.hsplit(newarr, 3)
print("\nhsplitted array:")
print(hsplitted_arr)

vsplitted_arr = np.vsplit(newarr, 3)
print("\nvsplitted array:")
print(vsplitted_arr)

