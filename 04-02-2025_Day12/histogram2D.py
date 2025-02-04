import matplotlib.pyplot as plt

x=[3,2,3,3,5,6]
y=[7,8,7,7,11,12]
plt.hist2d(x,y,bins=7,weights=[5,7,9,10,1,99],cmin=1,cmax=10)
plt.show()