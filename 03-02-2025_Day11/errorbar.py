import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.0, 2.5, 1.8, 3.2, 2.7])
y_err = np.array([0.2, 0.3, 0.15, 0.25, 0.2])  
x_err = np.array([0.1, 0.2, 0.1, 0.15, 0.1])

plt.errorbar(x, y, yerr=y_err,xerr=x_err, fmt='o', capsize=5, label='Data with Error Bars')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.show()
