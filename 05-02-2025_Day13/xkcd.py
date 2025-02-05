import matplotlib.pyplot as plt
# Enabling XKCD mode
plt.xkcd()

# Creating an XKCD style pie chart
sizes = [15, 30, 45, 10]
plt.pie(sizes, labels=['A', 'B', 'C', 'D'], autopct='%1.1f%%', startangle=140)
plt.title('XKCD Style Pie Chart')
plt.show()