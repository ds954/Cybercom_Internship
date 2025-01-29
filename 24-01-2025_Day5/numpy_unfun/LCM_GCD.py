import numpy as np

arr = np.arange(1, 11)
arr1=np.array([4,8,2])

print("lcm: ",np.lcm.reduce(arr1))
print("lcm of 1 to 9: ",np.lcm.reduce(arr))

print("gcd: ",np.gcd.reduce(arr1))
print("gcd of 1 to 9: ",np.gcd.reduce(arr))