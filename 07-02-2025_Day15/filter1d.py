from scipy import ndimage, datasets
import matplotlib.pyplot as plt

# Load an example image from datasets
ascent = datasets.face()

# Apply a 1D Gaussian filter along the x-axis (axis=0)
filtered_image = ndimage.gaussian_filter1d(ascent, sigma=2, axis=0)

# Plot the original and filtered image
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(ascent, cmap='gray')
axs[0].set_title('Original Image')
axs[1].imshow(filtered_image, cmap='gray')
axs[1].set_title('1D Gaussian Filtered Image')

plt.show()
