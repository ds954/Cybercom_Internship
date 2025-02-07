from scipy import ndimage, datasets
import matplotlib.pyplot as plt

# Load an example image from datasets
ascent = datasets.face()

# Apply Gaussian gradient magnitude filter with sigma=2
gradient_magnitude = ndimage.gaussian_gradient_magnitude(ascent, sigma=1)

# Plot the original and gradient magnitude image
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(ascent, cmap='gray')
axs[0].set_title('Original Image')
axs[1].imshow(gradient_magnitude, cmap='gray')
axs[1].set_title('Gaussian Gradient Magnitude')

plt.show()
