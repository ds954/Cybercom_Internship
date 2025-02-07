from scipy.ndimage import convolve1d
import numpy as np

print(convolve1d([1,2,1,1,0,1,2,2,1], weights=[-1,1,2],mode='constant',cval=1))
padded_arr = np.pad([1,2,1,1,0,1,2,2,1], pad_width=1, mode='constant',constant_values=1)
print(padded_arr)