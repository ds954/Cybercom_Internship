# Write a function basic_array_operations(arr) that:
# Calculates the square root of each element in the array.
# Calculates the sine of each element.
# Returns both results as separate arrays.

import numpy as np
def basic_array_operations(arr):
    squred_root=np.sqrt(arr)
    sine_arr=np.sin(arr)
    print("square root:",squred_root)
    print("sine",sine_arr)



arr=np.array([4,9,16,25,36,49,64,81,100])
basic_array_operations(arr)