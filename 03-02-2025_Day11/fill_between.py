import matplotlib.pyplot as plt

# Define lists for x and corresponding y values
x = [2, 4, 6]
y = [1, 2, 3]
z = [4, 16, 36]
a = [5, 7, 9]

# Plot the lines separately
plt.plot(x, y, marker='o', label='y-values')
plt.plot(x, z, marker='o', label='z-values')
plt.plot(x, a, marker='o', label='a-values')

# Fill between z and a
plt.fill_between(x, z, a, color='purple', alpha=0.4,where=[(z[i] < 20 and a[i] < 8) for i in range(len(x))])

# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Fill Between Example")
plt.legend()

# Show the plot
plt.show()
