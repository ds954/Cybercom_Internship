import numpy as np

arr1=np.array([1,2,3])
arr2=np.array([10,20,30])
# [10,10]

print("summation methods:")
print("sum: ",np.sum([arr1,arr2]))
print("sum on axis 1: ",np.sum([arr1,arr2],axis=1))
print("cumulative sum: ",np.cumsum([arr1,arr2],axis=1))

print("\nproduct methods:")
print("product: ",np.prod([arr1,arr2]))
print("product on axis 1: ",np.prod([arr1,arr2],axis=1))
print("cumulative product: ",np.cumprod([arr1,arr2],axis=1))

print("\nDiffrence method:")
print("differnce: ",np.diff(arr2, n=2))
