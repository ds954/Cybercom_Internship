import numpy as np

arr = np.array([1, 2, 3])

#corresponding index of the element while iterating,
for idx, x in np.ndenumerate(arr):
  print(idx, x)