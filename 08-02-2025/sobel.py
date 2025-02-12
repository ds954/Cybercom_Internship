import scipy.ndimage as nd  
import matplotlib.pyplot as plt  
import numpy as np

im = np.zeros((256, 256))  
im[64:-64, 64:-64] = 1  
im[90:-90,90:-90] = 2  
im = nd.gaussian_filter(im, 8)  
zx = nd.sobel(im, axis = 0, mode = 'constant')  
zy = nd.sobel(im, axis = 1, mode = 'constant')  
sobl = np.hypot(zx, zy)  
plt.imshow(sobl)  
plt.show()  