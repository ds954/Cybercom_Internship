import matplotlib.pyplot as plt
import numpy as np
# X-axis represents the bin ranges while the Y-axis gives information about frequency.
# distribution of element

x1 = np.random.randint(0, 10, 100)
x2 = np.random.randint(0, 10, 100)
plt.hist([x1, x2],bins=5, histtype='bar',align='mid',label='CPI Hist')
plt.legend()
plt.show()