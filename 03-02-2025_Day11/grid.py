import matplotlib.pyplot as plt
import numpy as np

x=np.array([1,2,3,4])
y=np.array([1,4,9,16])


font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.xlabel("Value",fontdict=font2)
plt.ylabel("Squred Value",fontdict=font2)
plt.title("Graph",fontdict=font1)
plt.plot(x,y,marker='o')
plt.grid(axis='x',c='m',ls="-.",lw=1)
plt.show()