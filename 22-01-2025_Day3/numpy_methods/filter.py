import numpy as np

arr = np.array([5,6,7,8])
filtered_arr=[] #create empty array

for element in arr:
    if element>6: 
        #if condition is true then append true into filtered_arr
        filtered_arr.append(True)
    else:
        # append false to filtered_arr
        filtered_arr.append(False)

print(filtered_arr) #return boolean list

#return a new array where only elements corresponding to 'True' in the filtered_arr are included
resultArray=arr[filtered_arr]
#print elements that greater then 6
print(resultArray)

false_values = arr[~np.array(filtered_arr)]  # ~ is used to negate the boolean array
print("Elements less than or equal to 6:", false_values)