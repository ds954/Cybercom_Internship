import numpy as np

arr=np.array([[[1,2],[3,4]],
              [[5,6],[7,8]]])

# iterating through each scalar of an array
for i in np.nditer(arr):
    print(i)

#To change data type of array element op_dtypes argument is pass to nditer() method
#numpy does not change data type of array in-place so flags=['buffered'] is passed to get extra space for change data type
for x in np.nditer(arr, flags=['buffered'], op_dtypes=['S']):
  print(x)


