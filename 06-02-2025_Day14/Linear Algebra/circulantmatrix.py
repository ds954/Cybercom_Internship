import numpy as np
from scipy.linalg import solve_circulant, solve, circulant, lstsq
from scipy.fft import ifft,fft


#  C x = b for x, where C is a circulant matrix
c = np.array([[1, 5, 3],
              [3, 1, 5],
              [5, 3, 1]])
b = np.array([1, 2, 3])
x=solve_circulant(c, b)
print(x)
y = ifft(fft(b) / fft(c))
print(y)