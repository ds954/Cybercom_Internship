import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4])
y = np.array([1, 2, 3, 4])
x1 = np.array([4, 3, 2, 1])
y1 = np.array([1, 4, 9, 16])
plt.subplot(2,1,1)
plt.plot(x,y)
plt.title("Sales")


plt.subplot(2,1,2)
plt.plot(x1,y1)
plt.title("income")


font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.suptitle("MY SHOP")
# plt.plot(x,y,marker='o')
plt.show()