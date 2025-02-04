import matplotlib.pyplot as plt
from sklearn import datasets 
import numpy as np
import pandas as pd

wine=datasets.load_wine()
wine_df=pd.DataFrame(wine.data,columns=wine.feature_names)
wine_df["wine_type"]=wine.target
print(wine_df.head())


fig=plt.figure(figsize=(5,3))
axs=fig.add_subplot(1,1,1)
axs.spines[["bottom","top","left","right"]].set_visible(True)

plt.xlabel("Alcohol",fontsize=16,fontweight="bold")
plt.ylabel("malic_acid",fontsize=16,fontweight="bold")
plt.title("Alcohol vs malic_acid",fontsize=25,fontweight="bold")
plt.hexbin(x=wine_df["alcohol"],y=wine_df["malic_acid"],gridsize=(15,10),linewidths=1.5,edgecolors="white",mincnt=2,C=wine_df["wine_type"],reduce_C_function=np.max)
plt.show()
