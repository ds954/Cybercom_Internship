import matplotlib.pyplot as plt
import numpy as np

# theta is an array representing the angles in radians for data points.
# r is an array representing the radial distance from the center for each data point.
theta = np.linspace(0, 2*np.pi, 20)
r = np.array([0.2, 0.5, 0.8, 1.2, 1.5, 1.8, 2.1, 2.5, 2.8, 3.0, 2.8, 2.5, 2.1, 1.8, 1.5, 1.2, 0.8, 0.5, 0.2, 0.0])

plt.polar(theta,r,label='sine',marker='o', linestyle='None')
plt.legend()
plt.show()