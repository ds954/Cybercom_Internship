import matplotlib.pyplot as plt
import numpy as np

# Create a sample image (3x3 matrix)
image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Create a figure to display all the images side by side
plt.figure(figsize=(12, 8))

# 'nearest' interpolation: Each pixel is assigned the value of the nearest pixel in the original image.
plt.subplot(3, 3, 1)
plt.imshow(image, interpolation='nearest')
plt.title('Nearest')
# Nearest neighbor interpolation looks blocky as it copies the value of the nearest pixel

# 'bilinear' interpolation: Uses linear interpolation between the nearest 2 pixels.
plt.subplot(3, 3, 2)
plt.imshow(image, interpolation='bilinear')
plt.title('Bilinear')
# Bilinear interpolation provides smoother results than nearest by averaging the values of the closest pixels.

# 'bicubic' interpolation: Uses cubic interpolation for a smoother and sharper result than bilinear.
plt.subplot(3, 3, 3)
plt.imshow(image, interpolation='bicubic')
plt.title('Bicubic')
# Bicubic interpolation uses a more complex algorithm, providing even smoother transitions and less pixelation.

# 'spline16' interpolation: Uses spline interpolation with 16 coefficients for a smoother result.
plt.subplot(3, 3, 4)
plt.imshow(image, interpolation='spline16')
plt.title('Spline16')
# Spline16 creates a smooth curve between pixels, improving image quality during resizing.

# 'spline36' interpolation: Similar to spline16 but with 36 coefficients for higher quality.
plt.subplot(3, 3, 5)
plt.imshow(image, interpolation='spline36')
plt.title('Spline36')
# This is a higher-quality version of spline interpolation with more coefficients.

# 'hanning' interpolation: Uses the Hanning windowed sinc function for interpolation.
plt.subplot(3, 3, 6)
plt.imshow(image, interpolation='hanning')
plt.title('Hanning')
# Hanning interpolation is a type of windowed sinc interpolation, which is often used in signal processing.

# 'hamming' interpolation: Uses the Hamming windowed sinc function.
plt.subplot(3, 3, 7)
plt.imshow(image, interpolation='hamming')
plt.title('Hamming')
# Hamming interpolation provides smoother results with less ringing compared to other windowed sinc functions.

# 'lanczos' interpolation: High-quality interpolation often used for downsampling.
plt.subplot(3, 3, 8)
plt.imshow(image, interpolation='lanczos')
plt.title('Lanczos')
# Lanczos is known for giving sharp and high-quality results, especially when downscaling images.

# 'gaussian' interpolation: Uses the Gaussian windowed sinc function for interpolation.
plt.subplot(3, 3, 9)
plt.imshow(image, interpolation='gaussian')
plt.title('Gaussian')
# Gaussian interpolation is known for smooth results, but may blur finer details.

# Display the images
plt.tight_layout()
plt.show()
