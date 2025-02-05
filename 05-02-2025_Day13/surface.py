import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4])  
y = np.array([1, 3, 5, 7])  
X,Y=np.meshgrid(x,y)
print(X)
print(Y)
z=X**2+Y**2
print(z)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(X,Y,z)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.show()