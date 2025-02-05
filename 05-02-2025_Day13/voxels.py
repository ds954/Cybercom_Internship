import numpy as np
import matplotlib.pyplot as plt

voxels = np.array([[[1,1,0,1],
                    [0,0,0,0],
                    [1,0,-5,0]]])

# Create figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the voxel grid
ax.voxels(voxels, edgecolor='black', facecolors='cyan')

# Label the axes
ax.set_xlabel("X-axis (left-right)")
ax.set_ylabel("Y-axis (front-back)")
ax.set_zlabel("Z-axis (bottom-top)")
ax.set_title("3D Voxel Grid")

plt.show()
