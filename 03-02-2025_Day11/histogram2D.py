import matplotlib.pyplot as plt

x=[1,2,3,4,5,6]
y=[7,8,9,10,11,12]
plt.hist2d(x,y,bins=7,weights=[5,7,9,10,1,99],cmin=1,cmax=10)
plt.show()