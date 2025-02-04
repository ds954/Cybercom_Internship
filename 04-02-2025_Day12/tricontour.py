import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

x = np.random.rand(100) * 20
y = np.random.rand(100) * 20
z = np.sin(x) * np.cos(y) 


triang = tri.Triangulation(x, y)


plt.figure(figsize=(8, 6))
plt.tricontour(triang, z, cmap="viridis")  
plt.tricontourf(triang, z, cmap="viridis")  

plt.colorbar()
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
