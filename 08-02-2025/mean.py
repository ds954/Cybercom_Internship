from scipy import ndimage
import numpy as np

a = np.arange(25).reshape((5,5))
labels = np.zeros_like(a)
labels[3:5,3:5] = 1
index = np.unique(labels)
print(labels)
print(index)
result=ndimage.mean(a, labels=labels, index=index)
print(result)