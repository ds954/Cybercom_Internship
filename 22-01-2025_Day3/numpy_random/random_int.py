from numpy import random

print_random_int=random.randint(100) #return random number 
print(f"random int: {print_random_int}")

random_float=random.rand() #return random float number between 0 and 1
print(f" random float: {random_float}")

random_int=random.randint(100,size=(5)) #return array with size 5 
print(f"1D Array of Random Integers: {random_int}")

shape_1D_arr=random.rand(5) #return 1D array with size 5
print(f"1D Array of Random Floats: {shape_1D_arr}")

shape_2D_arr=random.rand(2,4) #return 2D array,each array contain 4 elements
print(f"2D Array of Random Floats (2x4): \n {shape_2D_arr}")

x=random.choice([3, 5, 7, 9], size=(3, 5)) #return 3x5 array consists of the values in the array parameter
print(f"3x5 Array of Random Choices: \n {x}")

x=random.choice([3, 5, 7, 9],p=[0.2,0.4,0.0,0.4], size=(3, 5)) #return 3x5 array consists of the values in the array parameter
print(f"3x5 Array of Random Choices: \n {x}") #7 will not print as probability set as 0




