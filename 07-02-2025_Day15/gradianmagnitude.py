from scipy import ndimage, datasets
import matplotlib.pyplot as plt

ascent = datasets.ascent()

fig, axs = plt.subplots(2, 2, figsize=(8, 8))
plt.gray()

result = ndimage.gaussian_gradient_magnitude(ascent, sigma=5)
result1= ndimage.gaussian_laplace(ascent, sigma=3)
result2 = ndimage.gaussian_laplace(ascent, sigma=1)

axs[0, 0].imshow(ascent, aspect='auto')
axs[0, 1].imshow(result, aspect='auto')
axs[1, 0].imshow(result1, aspect='auto')
axs[1, 1].imshow(result2, aspect='auto')

plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()