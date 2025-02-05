import matplotlib.pyplot as plt
import numpy as np 

x=np.linspace(0,10,20)
y=np.linspace(0,10,20)

X,Y=np.meshgrid(x,y)
u = np.sin(X)*Y
v = np.cos(Y)*Y

fig,ax=plt.subplots(figsize=(15,8))
ax.quiver(X, Y, u, v)


ax.axis([-0.3, 2.3, -0.3, 2.3])
ax.set_title('Meshgrid Quiver Plot')
 
plt.show()