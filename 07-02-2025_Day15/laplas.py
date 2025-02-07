from scipy import ndimage, datasets
import matplotlib.pyplot as plt

# Load an example image from datasets
ascent = datasets.face()

# Apply Gaussian Laplace filter with sigma=2
laplace_filtered = ndimage.gaussian_laplace(ascent, sigma=2)

# Plot the original and Laplace filtered image
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(ascent, cmap='gray')
axs[0].set_title('Original Image')
axs[1].imshow(laplace_filtered, cmap='gray')
axs[1].set_title('Gaussian Laplace Filtered Image')

plt.show()
