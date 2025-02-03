import matplotlib.pyplot as plt  
import numpy as np  
  
np.random.seed(10)  
  
dataSet1 = np.random.normal(100, 10, 220)  
dataSet2 = np.random.normal(80, 20, 200)  
dataSet3 = np.random.normal(60, 35, 220)  
dataSet4 = np.random.normal(50, 40, 200)  
dataSet = [dataSet1, dataSet2, dataSet3, dataSet4]  
  
figure = plt.figure(figsize =(5,3))  
ax = figure.add_axes([0, 0, 1, 1])  
bp = ax.boxplot(dataSet)  
plt.show() 