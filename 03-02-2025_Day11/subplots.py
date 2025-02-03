import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4])
y1 = np.array([1, 2, 3, 4])
y2 = np.array([4, 3, 2, 1])

fig, axs = plt.subplots(2, 2, figsize=(8, 6))

# Plotting on individual axes
axs[0, 0].plot(x, y1)
axs[0, 0].set_title('Linear')

axs[0, 1].plot(x, y2)
axs[0, 1].set_title('Inverse')

axs[1, 0].plot(x, y1)
axs[1, 0].set_title('Linear Again')

axs[1,1].plot(x,y2)
axs[1,1].set_title("Inverse Again")
fig.suptitle("Plot")
plt.subplots_adjust(wspace=0.3, hspace=0.3)


plt.show()