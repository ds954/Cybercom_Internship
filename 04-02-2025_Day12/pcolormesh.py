import matplotlib.pyplot as plt
import numpy as np

arr1=np.array([[0,0,0],
               [1,1,1],
               [2,2,2]])
arr2=np.array([[0,1,2],
               [0,1,2],
               [0,1,2]])
arr3=np.array([[0,0.5,1],
               [1,1.5,2],
               [2,2.5,3]])
# plt.imshow(arr3)
plt.pcolormesh(arr1,arr2,arr3)
plt.colorbar()
plt.show()