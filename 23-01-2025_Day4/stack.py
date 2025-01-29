import numpy as np

# Define two 1D arrays
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([10, 11, 12, 13])

# Stack along axis 0 
stack_array0 = np.stack((arr1, arr2), axis=0)
print("Stacked 1D arrays along axis 0: \n", stack_array0)

# Stack along axis 1 )
stack_array1 = np.stack((arr1, arr2), axis=1)
print("Stacked 1D arrays along axis 1: \n", stack_array1)

# Define two 2D arrays
arr3_2D = np.array([[21, 22, 23, 24],
                    [25, 26, 27, 28]])
arr4_2D = np.array([[31, 32, 33, 34],
                    [35, 36, 37, 38]])

# Stack 2D arrays along axis 0 
stack_array_0= np.stack((arr3_2D, arr4_2D), axis=0)
print("Stacked 2D arrays along axis 0: \n", stack_array_0)

# Stack 2D arrays along axis 1 
stack_array_1 = np.stack((arr3_2D, arr4_2D), axis=1)
print("Stacked 2D arrays along axis 1: \n", stack_array_1)

# Stack 2D arrays along axis 2
stack_array_2= np.stack((arr3_2D, arr4_2D), axis=2)
print("Stacked 2D arrays along axis 2: \n", stack_array_2)

# Define two 3D arrays
arr5_3D = np.array([[[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]],
                    
                    [[21, 22, 23],
                     [24, 25, 26],
                     [28, 29, 30]]])

arr6_3D = np.array([[[10, 11, 21],
                     [12, 13, 22],
                     [14, 15, 23]],
                    
                    [[31, 32, 33],
                     [34, 35, 36],
                     [37, 38, 39]]])

# Stack 3D arrays along axis 0 
stack_arr_3D_0 = np.stack((arr5_3D, arr6_3D), axis=0)
print("Stacked 3D arrays along axis 0: \n", stack_arr_3D_0)

# Stack 3D arrays along axis 1 
stack_arr_3D_1 = np.stack((arr5_3D, arr6_3D), axis=1)
print("Stacked 3D arrays along axis 1: \n", stack_arr_3D_1)

# Stack 3D arrays along axis 2 
stack_arr_3D_2 = np.stack((arr5_3D, arr6_3D), axis=2)
print("Stacked 3D arrays along axis 2: \n", stack_arr_3D_2)

# Stack 3D arrays along axis 3 
stack_arr_3D_3 = np.stack((arr5_3D, arr6_3D), axis=3)
print("Stacked 3D arrays along axis 3: \n", stack_arr_3D_3)
