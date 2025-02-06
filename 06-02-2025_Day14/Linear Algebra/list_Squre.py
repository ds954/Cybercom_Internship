from scipy.linalg import lstsq
import numpy as np

x = np.array([1, 2.5, 3.5, 4, 5, 7, 8.5])
y = np.array([0.3, 1.1, 1.5, 2.0, 3.2, 6.6, 8.6])
M = x[:, np.newaxis]**[0, 2]
print(M)


p, res, rnk, s = lstsq(M, y)
print(p)
print(res)
print(rnk)
print(s)