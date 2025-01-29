import numpy as np

arr = np.array([-1, 0, 1])
newarr = arr.astype(bool)
print(newarr)
print(newarr.dtype)

#Copy vs View
arr = np.array([1, 2, 3, 4, 5])
x = arr.copy()
y = arr.view()
x[0]=3 # can not change original array
print(arr)
print(x)
y[1]=45 #hange original array
print(arr)
print(y)
#To check it owns data or not
print(x.base) # return none
print(y.base) # return original array

