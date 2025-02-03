import matplotlib.pyplot as plt

value1=[2,4,5,7,8]
value2=[11,12,45,78,8]

plt.stem(value1,value2,linefmt ='-.',markerfmt='H')
plt.show()