import matplotlib.pyplot as plt
import numpy as np
#  plot identical lines at a given position

positions=[2,4,6]
offsets=[3]

plt.eventplot(positions, lineoffsets=offsets,linelengths=2,linewidths=5,linestyles='dashdot',orientation='vertical', color = [(0.5,0.5,0.8)]) 
plt.show()