import matplotlib.pyplot as plt
import numpy as np

x = np.array([0, 1, 2, 3, 0.5, 1.5, 2.5, 1, 2, 1.5])
y = np.array([0, 0, 0, 0, 1.0, 1.0, 1.0, 2, 2, 3.0])

z = np.cos(1.5 * x) * np.cos(1.5 * y)
plt.tripcolor(x,y,z)
plt.colorbar()
plt.show()
