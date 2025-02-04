import matplotlib.pyplot as plt
import numpy as np

data = [np.random.normal(0, std, 100) for std in range(1, 5)]
data1=np.random.normal(0,1,100)
plt.violinplot(data1,vert=True,showextrema=True,showmeans=True,showmedians=True,quantiles=[[0.25,0.50,0.75]])
plt.show()