# Create a function customized_plot(x, y) that plots a line graph with the following customizations:
# Title: "Customized Line Plot"
# X-axis label: "X Axis"
# Y-axis label: "Y Axis"
# Line style: Dashed
# Line color: Red

import matplotlib.pyplot as plt
def customized_plot(x,y):
    plt.plot(x,y,ls='dashed',color='Red')
    plt.title("Customized Line Plot")
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    plt.show()

x=[1,2,3,4]
y=[2,4,6,8]
customized_plot(x,y)


