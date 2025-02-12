import numpy as np
from scipy import ndimage

a = np.arange(16).reshape((4,4))
print(a)

labels = np.zeros_like(a)
labels[:2,:2] = 1
labels[2:, 1:3] = 2

print(labels)

result1=ndimage.maximum(a)
result2=ndimage.maximum(a, labels=labels, index=[1,2])
result3=ndimage.maximum(a, labels=labels)
print(result1)
print(result2)
print(result3)