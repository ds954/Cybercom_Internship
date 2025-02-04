import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-2, 5, 100)
y = np.linspace(-2, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig = plt.figure(figsize=(14, 6))  


ax1 = fig.add_subplot(121, projection="3d")
ax1.plot_surface(X, Y, Z, cmap='viridis')
ax1.set_title("3D Surface Plot")


ax2 = fig.add_subplot(122)
contour = ax2.contourf(X, Y, Z, cmap='viridis')
plt.colorbar(contour, ax=ax2) 
ax2.set_title("Contour Plot")


plt.subplots_adjust(wspace=0.4)  


plt.show()
