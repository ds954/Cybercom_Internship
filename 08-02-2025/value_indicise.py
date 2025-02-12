import numpy as np
from scipy import ndimage    

a=np.array([[2, 2, 2, 0, 0, 3],
       [2, 2, 2, 0, 0, 0],
       [0, 0, 1, 1, 0, 0],
       [0, 0, 1, 1, 0, 0],
       [0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0]])

val_indices = ndimage.value_indices(a)
print(val_indices)
print(val_indices.keys())
ndx1 = val_indices[1]
print(ndx1)
print(a[ndx1])