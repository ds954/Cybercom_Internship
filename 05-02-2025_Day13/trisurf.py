import matplotlib.pyplot as plt
import numpy as np

# Define x and y values
x = np.array([1, 2, 3, 4, 1.5, 2.5, 3.5, 2, 3, 2.5])  
y = np.array([1, 3, 5, 7, 2, 4, 6, 5, 3, 5])  

# Compute Z values
z = x**2 + y**2  

# Create figure and 3D subplot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Plot the triangulated surface
t=ax.plot_trisurf(x, y, z, cmap="viridis", edgecolor="black", alpha=0.8)

# Labels
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Triangular Surface Plot")
plt.colorbar(t)
plt.show()
