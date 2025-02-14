'''
positional arguments:
    positional argument passed to a function based on its position
Keyword arguments:
    parameter-name and value (key:value) pair passed to a function
'''

def fun(name,age):
    print(f"Hello, my name is {name} and I am {age} years old.")
fun('dhara',20) #positional argument
fun(age=20,name='xyz') #keyword argument


