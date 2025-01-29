import numpy as np

arr=np.array([1,2,3,1,3,5,2,5,1])
print(np.unique(arr))

arr1=np.array([1,2,3])
arr2=np.array([4,3,6,10])

print(np.union1d(arr1,arr2))
print(np.intersect1d(arr1,arr2,assume_unique=True))
print(np.setdiff1d(arr1,arr2,assume_unique=True))
print(np.setxor1d(arr1,arr2,assume_unique=True))

