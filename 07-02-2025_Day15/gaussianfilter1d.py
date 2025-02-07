from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
import numpy as np

original_data=np.array([4,2,3,7,6,9,4])
sigma_1=gaussian_filter1d(original_data,1)
sigma_5=gaussian_filter1d(original_data,5)
print(sigma_1)
print(sigma_5)
plt.plot(original_data,'ko',label='original data',linestyle='solid')
plt.plot(sigma_1,'-x',label='filttered singma 1')
plt.plot(sigma_5,'-.D',label='filttered singma 5')
plt.legend()
plt.show()
