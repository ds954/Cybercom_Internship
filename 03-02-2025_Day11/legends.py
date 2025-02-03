import matplotlib.pyplot as plt

values1 = [5,8,9,4,1,6,7,2,3,8]
values2 = [8,3,2,7,6,1,4,9,8,5]
plt.plot(values1)
plt.plot(values2)
plt.xlabel('Roll No')
plt.ylabel('CPI')
plt.scatter(5,1, color='red', s=50)
plt.annotate('Lowest CPI', xy=(5,1), xytext=(6, 3),
             arrowprops=dict(facecolor='red', shrink=0.05),
             fontsize=12, color='red')
plt.legend(['CX','CY'],loc=4)
plt.show()