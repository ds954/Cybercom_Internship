from scipy import ndimage as nd
import numpy as np

a = np.array([[1, 2, 0, 0],
              [5, 3, 0, 4],
              [0, 0, 0, 7],
              [9, 3, 0, 0]])
labels, labels_nb = nd.label(a)
print(labels)
result1=nd.minimum(a, labels=labels, index=np.arange(1, labels_nb + 1))
result2=nd.minimum(a)
result3=nd.minimum(a, labels=labels)

print(result1)
print(result2)
print(result3)