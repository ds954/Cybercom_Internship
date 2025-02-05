import matplotlib.pyplot as plt
import numpy as np
     
x = np.linspace(0, 15, 5)
X, Y = np.meshgrid(x, x)
U, V = X**2, Y**2
 
fig1, axs1 = plt.subplots()
axs1.barbs(X, Y, U, V, U * 2, fill_empty = True)
 
axs1.set_title('matplotlib.axes.Axes.barbs()\
 Example', fontsize = 14, fontweight ='bold')
plt.show()