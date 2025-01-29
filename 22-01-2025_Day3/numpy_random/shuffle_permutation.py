import numpy as np
from numpy import random

arr=np.array([88,72,12,52])
shuffled_array=random.shuffle(arr) #it makes changes to the original array.
print("shuffled array is: ",arr)

newarr=np.array([12,25,20,99])
print("permuted array is: ",random.permutation(newarr) )#leaves the original array un-changed.
