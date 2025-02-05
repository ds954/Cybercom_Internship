import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()


ellipse = patches.Ellipse((0, 0), 3, 2, edgecolor='g', facecolor='yellow',angle=45)
ax.add_patch(ellipse)

plt.title('Ellipse with Custom Colors')
 
plt.axis('equal') 
plt.show()