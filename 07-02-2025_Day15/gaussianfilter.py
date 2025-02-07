import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# Create a simple 2D array (image)
image = np.array([[1, 1, 1, 1, 1],
                  [1, 2, 2, 2, 1],
                  [1, 2, 3, 2, 1],
                  [1, 2, 2, 2, 1],
                  [1, 1, 1, 1, 1]])

# Apply Gaussian filter
sigma = 1 # Standard deviation for the Gaussian kernel
filtered_image = ndimage.gaussian_filter(image, sigma)

# Plot the original and filtered images
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
t=axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original Image')
axes[0].axis('off')

axes[1].imshow(filtered_image, cmap='gray')
axes[1].set_title('Filtered Image with Gaussian Filter')
axes[1].axis('off')
plt.colorbar(t)
plt.show()
