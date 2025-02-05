import matplotlib.pyplot as plt

# Creating a line and a circle
# line = plt.plot([0, 1], [0, 1], color='blue', linewidth=2, label='Line')
circle = plt.Circle((0.5, 0.5), 0.1, color='red', label='Circle')

# Setting different z-orders
# circle.set_zorder(1)
# line.set_zorder(2)

# Adding elements to the plot
# plt.gca().add_patch(circle)
plt.legend()

# Displaying the plot
plt.title('Controlling Drawing Order with zorder')
plt.show()