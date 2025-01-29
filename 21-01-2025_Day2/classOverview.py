# Class 'value' with a class variable 'x'
class value:
    x = 3  # Class variable 'x' is set to 3

# Create an instance of the class and print the value of 'x'
print(value().x)  # Output: 3, accessing the class variable 'x'

# __init__() method:
# This function is called automatically every time a new object of the class is created.

class Person:
    def __init__(self, name, age):  # Constructor that initializes the object with name and age
        self.name = name  # Assign name to the object
        self.age = age    # Assign age to the object

# Creating an object of Person class
p1 = Person("abc", 20)

# Accessing attributes of the object
print(p1.name)  # Output: 'abc'
print(p1.age)   # Output: 20

# __str__() method:
# This method is used to represent the object as a string when the object is printed.

class person1:
    def __init__(self, name, age):  # Constructor to initialize the object's name and age
        self.name = name
        self.age = age

    def __str__(self):  # This method is called when printing the object
        return f"name:{self.name}, age:{self.age}"  # Custom string representation

# Creating an object of person1
p1 = person1('xyz', 85)
print(p1)  # Output: 'name:xyz, age:85'

# Changing the value of name attribute
p1.name = 'abc'
print(p1)  # Output: 'name:abc, age:85'

# Deleting the age attribute from the object
del p1.age
# Printing the name after deletion of age
print(p1.name)  # Output: 'abc', age is deleted, so it won't print
