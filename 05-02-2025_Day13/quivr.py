import matplotlib.pyplot as plt
import numpy as np 

x_pos = 1
y_pos = 1
x_direct = 2
y_direct = 1


fig, ax = plt.subplots(figsize=(12, 7))

ax.quiver(x_pos, y_pos, x_direct, y_direct, angles='xy', scale_units='xy', scale=5, color='green', width=0.02, label='Arrow')


ax.set_xlim([0, 4])
ax.set_ylim([0, 3])
ax.set_title('Basic Quiver Plot')
plt.legend()

plt.show()