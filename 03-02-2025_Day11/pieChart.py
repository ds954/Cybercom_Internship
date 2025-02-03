import matplotlib.pyplot as plt


labels = ['Python', 'Java', 'C++', 'JavaScript']
sizes = [40, 25, 20, 15]  # Percentage distribution
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

# Exploding the first slice (Python)
explode = (0.1,0,0,0)  


plt.pie(sizes, labels=labels, colors=colors,
        explode=explode, shadow=True, startangle=10)


plt.title("Programming Language ")
plt.legend(title="Language",loc=4)
plt.show()
