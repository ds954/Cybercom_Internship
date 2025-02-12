from scipy import ndimage
import numpy as np
a = np.array([[5, 2, 0, 0],
              [5, 3, 0, 4],
              [0, 25, 0, 7],
              [9, 3, 0, 0]])
result=ndimage.standard_deviation(a)
print(result)