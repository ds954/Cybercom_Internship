# Write a function plot_subplots(x, y1, y2) to plot two subplots:
# The first subplot should be a line plot.
# The second subplot should be a scatter plot.
# Ensure both plots share the same x values.

import matplotlib.pyplot as plt
def plot_subplots(x,y1,y2):
    fig,ax=plt.subplots(2,1,sharex=True)
    ax[0].plot(x,y1)
    ax[0].set_title("line")

    ax[1].scatter(x,y2)
    ax[1].set_title("Scatter")

    plt.show()
x=[1,2,3,4,5,6]
y1=[2,4,6,8,10,12]
y2=[5,7,8,6,10,11]
plot_subplots(x,y1,y2)

    
