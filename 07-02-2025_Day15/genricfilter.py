from scipy import ndimage, datasets
import matplotlib.pyplot as plt
import numpy as np

# Load the ascent image
ascent = datasets.face()

# Define a custom function to calculate the mean of the values in the window
def mean_filter(values):
    return np.mean(values)

# Apply the generic_filter with a 5x5 neighborhood and the custom mean function
result = ndimage.generic_filter(ascent, mean_filter, size=5)

# Plot the original and filtered images
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(ascent, cmap='gray')
axs[0].set_title('Original Image')
axs[1].imshow(result, cmap='gray')
axs[1].set_title('Filtered Image (Mean Filter)')

plt.show()
