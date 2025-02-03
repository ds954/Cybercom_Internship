import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 3, 4, 5, 7])
y = np.array([1, 9, 16, 25, 49])

# Create the figure and subplots
fig, axes = plt.subplots(3, 1, figsize=(5,7),sharex=True)  

# where='post'
#  The step occurs after the x-coordinate. The y-value changes after you reach the x-coordinate.
axes[0].step(x, y, 'r*-', where='post')
axes[0].set_title("where='post'")
axes[0].grid(True)  # Add grid for readability

# where='pre'
# The step occurs before the x-coordinate. The y-value changes before you reach the x-coordinate.
axes[1].step(x, y, 'r*-', where='pre')
axes[1].set_title("where='pre'")
axes[1].grid(True)

# where='mid'
# The step between y=1 and y=9 is centered around x=3.
axes[2].step(x, y, 'r*-', where='mid')
axes[2].set_title("where='mid'")
axes[2].grid(True)



plt.show()