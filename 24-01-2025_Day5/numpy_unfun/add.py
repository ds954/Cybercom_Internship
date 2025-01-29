import numpy as np

arr1=np.array([5,6,7])
arr2=np.array([2,3,4])
z=[]
for i,j in zip(arr1,arr2):
    z.append(i+j)
print(z)

print("use add: ",np.add(arr1,arr2))
print("substtract: ",np.subtract(arr1,arr2))
print("divide: ",np.divide(arr1,arr2))
print("multiply: ",np.matmul(arr1,arr2))
print("multiply method 2: ",np.multiply(arr1,arr2))
print("power: ",np.power(arr1,arr2))
print("mod: ",np.mod(arr1,arr2))
print("remonder: ",np.remainder(arr1, arr2))
print("quotient and mod: ",np.divmod(arr1, arr2))

arr = np.array([-1, -2, 1, 2, 3, -4])

print("abs: ",np.absolute(arr)) 