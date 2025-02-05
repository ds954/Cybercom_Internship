import matplotlib.pyplot as plt

# Defining two 2D vectors
vector1 = [2, 3]
vector2 = [-1, 2]

# Plotting the vectors and their sum
plt.figure()
plt.quiver(0, 0, vector1[0], vector1[1], angles='xy', scale_units='xy', scale=1, color='mediumspringgreen', label='Vector 1')
plt.quiver(0, 0, vector2[0], vector2[1], angles='xy', scale_units='xy', scale=1, color='coral', label='Vector 2')
plt.quiver(0, 0, vector1[0] + vector2[0], vector1[1] + vector2[1], angles='xy', scale_units='xy', scale=1, color='saddlebrown', label='Vector 1 + Vector 2')

plt.xlim(-2, 4)
plt.ylim(-2, 5)
plt.title('Vector Addition')
plt.legend()
plt.grid(True)
plt.show()