from scipy import ndimage, datasets
import matplotlib.pyplot as plt
import numpy as np

# Load an example image from datasets
face = datasets.face()
flip_ud_face = np.flipud(face)  
rotate_face = ndimage.rotate(face, 30) #rotating the image 30 degree  
plt.imshow(rotate_face)
# plt.imshow(flip_ud_face)  
plt.show() 