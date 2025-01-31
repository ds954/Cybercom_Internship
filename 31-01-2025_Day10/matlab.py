import numpy as np
from scipy.cluster.hierarchy import ward, from_mlab_linkage
mZ = np.array([[1, 2, 1], 
               [4, 5, 1], 
               [7, 8, 1],
               [10, 11, 1], 
               [3, 13, 1.29099445],
               [6, 14, 1.29099445],
               [9, 15, 1.29099445],
               [12, 16, 1.29099445],
               [17, 18, 5.77350269],
               [19, 20, 5.77350269],
               [21, 22,  8.16496581]])
Z = from_mlab_linkage(mZ)
print(Z)