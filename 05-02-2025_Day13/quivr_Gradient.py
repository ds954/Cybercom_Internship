import matplotlib.pyplot as plt
import numpy as np 

x=np.linspace(0,10,50)
y=np.linspace(0,10,50)

X,Y=np.meshgrid(x,y)
z = np.sin(X) * np.cos(Y)
dx,dy=np.gradient(z)

fig,ax=plt.subplots(figsize=(10,7))
ax.quiver(X, Y, dx,dy)

ax.set_title('Meshgrid Quiver Plot')
 
plt.show()