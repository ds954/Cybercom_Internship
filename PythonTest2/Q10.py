# Create a function scatter_plot(x, y) that plots a scatter plot of the given x and y values.
import matplotlib.pyplot as plt


def scatter_plot(x,y):
    plt.scatter(x,y,marker='D',color='black')
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Scatter plot")
    plt.grid()
    plt.show()

x=[1,2,3,4,5,6]
y=[2,4,6,8,10,12]
scatter_plot(x,y)