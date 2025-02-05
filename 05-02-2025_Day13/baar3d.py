import matplotlib.pyplot as plt

x=[1,2,3]
z=[0,0,0]
y=[4,5,6]

dx=[1,1,1]
dy=[5,7,8]
dz=[3,3,3]

fig,ax=plt.subplots(subplot_kw={"projection": "3d"})
ax.bar3d(x,y,z,dx,dy,dz,color=['red','green','blue'])
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.show()