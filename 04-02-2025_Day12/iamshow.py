import matplotlib.pyplot as plt
import numpy as np
size=5
mylist=np.array([[0,1]*size,[1,0]*size]*size)
print(mylist)
# plt.imshow(mylist)
img=plt.imread("image.jpg")

# plt.axis(False)
plt.imshow(img[:,:,1],aspect='equal',alpha=0.8,origin='upper',interpolation='nearest')

plt.show()