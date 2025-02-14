# Create a function pie_chart(labels, sizes) to plot a pie chart. Add a legend and ensure one slice is "exploded" (slightly separated).

import matplotlib.pyplot as plt

def pie_chart(labels,sizes):
    plt.pie(sizes,explode=[0,0,0.1,0,0],labels=labels)
    plt.title("Pie Chart")
    plt.legend(title='pie')
    plt.show()
sizes=[10,20,30,40,50]
labels=['A','B','C','D','E']
pie_chart(labels,sizes)
