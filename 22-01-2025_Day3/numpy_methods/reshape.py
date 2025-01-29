import numpy as np

arr=np.array([1,2,3,4,5,6,7,8])
arr_2D=np.array([[1,2,3],
                 [4,5,6]])
print("2D array: ",arr_2D)
reshaped_arr=arr.reshape(2,4) # reshape array with 2 rows, each row has 4 element
print("array:",arr)
print("reshaped array: ",reshaped_arr)

#To get 1D array 2 methods
flatted_arr=reshaped_arr.reshape(-1) #convert multidimensional array into a 1D array.
print("Flatted array: ",flatted_arr) #return a copy
print("copy or view: ",flatted_arr.base)
ravel_arr=reshaped_arr.ravel()
print("array:",arr)

print("ravel array: ",ravel_arr) #return view
print("based array:",reshaped_arr)
#you do not have to specify an exact number for one of the dimensions
arr=np.array([1,2,3,4,5,6,7,8])
newarr = arr.reshape(2, 2, -1)  #numpy automatic consider -1 as 2 beacause there is 8 element 
print(newarr)


#Other methods
import numpy as np
sample_arr=np.array([[[1,2,3],
                     [4,5,6],
                     [7,8,9]]])
print("original array:")
print(sample_arr)

#To roatet 90 degree
roateted_arr=np.rot90(sample_arr) 
print("after roate 90 degree:")
print(roateted_arr)

#Reverses the elements along a given axis.
flipped_arr=np.flip(sample_arr)
print("Array flipped:")
print(flipped_arr)

#Flips the array left to right.
fliplr_arr = np.fliplr(sample_arr)
print("Array flipped left to right:")
print(fliplr_arr)

#Flips the array up to down
flipud_arr = np.flipud(sample_arr)
print("Array flipped up to down:")
print(flipud_arr)


