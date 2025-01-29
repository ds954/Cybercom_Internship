# Write a Program to create a 4×4 identity matrix.
import numpy as np

zeros=np.zeros((4,4))
zeros[0][0]=1
zeros[1][1]=1
zeros[2][2]=1
zeros[3][3]=1
print(zeros)
