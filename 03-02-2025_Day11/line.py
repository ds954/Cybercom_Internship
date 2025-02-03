import matplotlib.pyplot as plt
import numpy as np

# Data for first plot
x1 = np.array([2, 4, 8])
y1 = np.array([10, 12, 14])

# Data for second plot
x2 = np.array([1, 2, 3])
y2 = np.array([7, 8, 9])

# Plotting both lines
plt.plot(x1, y1, label='Line 1')  # Label for the first line
plt.plot(x2, y2, label='Line 2')  # Label for the second line

# Adding labels for the axes
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Adding title to the plot
plt.title('Multiple Lines with Labels and Legend')

# Adding legend to the plot
plt.legend()

# Displaying the plot
plt.show()
