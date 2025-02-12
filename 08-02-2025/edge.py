import scipy.ndimage as nd  
import numpy as np  
import matplotlib.pyplot as plt  

im = np.zeros((256, 256))  
im[64:-64, 64:-64] = 1  
im[90:-90,90:-90] = 2  
im = nd.gaussian_filter(im, 10)  
plt.imshow(im)  
plt.show()  