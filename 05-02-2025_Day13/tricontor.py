# Implementation of matplotlib function
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
	
# Create triangulation.
x = np.array([0, 1, 2, 3, 0.5, 1.5, 2.5, 1, 2, 1.5])
y = np.array([0, 0, 0, 0, 1.0, 1.0, 1.0, 2, 2, 3.0])
triangles = [[0, 1, 4], [1, 5, 4], [2, 6, 5], [4, 5, 7],
			[5, 6, 8], [5, 8, 7], [7, 8, 9], [1, 2, 5],
			[2, 3, 6]]

triang = mtri.Triangulation(x, y, triangles)
z = np.cos(1.5 * x) * np.cos(1.5 * y)
	
fig, axs = plt.subplots()
t = axs.tricontour(triang, z,colors ='white')
axs.tricontourf(triang, z )
plt.triplot(triang, 'bo-')

axs.set_title('tricontour Example')
plt.show()
