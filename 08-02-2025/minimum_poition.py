from scipy import ndimage
import numpy as np
a = np.array([[1, 2, 0, 0],
              [5, 3, 0, 4],
              [0, 0, 0, 7],
              [9, 3, 0, 0]])
result=ndimage.minimum_position(a)
print(result)