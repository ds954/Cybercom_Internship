# Write a NumPy Program to replace all even numbers in an array with -1.
import numpy as np

arr=np.array([1,2,3,4,5,6,7])

for i in range(len(arr)):
    if arr[i]%2==0:
        arr[i]=-1
        
print(arr)