# Demonstrating the use of the 'nonlocal' keyword

def myfunc1():
    x = "Hii"  # Variable 'x' is defined in the enclosing function 'myfunc1'
    def myfunc2():
        nonlocal x   # Declare 'x' as nonlocal so it refers to the 'x' in 'myfunc1'
        x = "hello"  # Modify the 'x' variable in the enclosing scope
    myfunc2()        # Call the inner function 'myfunc2' which modifies 'x'
    return x         # Return the modified value of 'x' from 'myfunc1'

print(myfunc1())  # Call 'myfunc1' and print the returned value
