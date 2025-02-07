import numpy as np
from scipy.spatial import procrustes

#
a = np.array([[0, 0], [1, 2], [2, 4], [3, 6]])  
b = np.array([[0, 0], [2, 3], [4, 6], [6, 9]]) 

# Perform Procrustes analysis
mtx1, mtx2, disparity = procrustes(a, b)

# Print the result
print("Transformed A (mtx1):\n", mtx1)
print("\nTransformed B (mtx2):\n", mtx2)
print("\nDisparity:", disparity)
