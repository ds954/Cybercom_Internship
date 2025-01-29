# Inheritance:
# A class 'child' can inherit attributes and methods from the 'parent' class.

class parent:
    def __init__(self, name, age):  # Constructor to initialize the parent's name and age
        self.firstname = name  # Assign first name to the object
        self.myage = age       # Assign age to the object

    def printdetails(self):  # Method to print details
        print(self.firstname, self.myage)

# Creating an object of the parent class
p = parent("qwe", 52)
p.printdetails()  # Output: 'qwe 52'

# Child class inheriting from parent class
# We can either call the parent constructor directly or use super().

# First child class using parent.__init__()
class child(parent):
    def __init__(self, name, age):  # Constructor to initialize name and age for child
        parent.__init__(self, name, age)  # Call parent's constructor explicitly

# Creating an object of child class
c = child("abc", 25)
c.printdetails()  # Output: 'abc 25', inherited from parent


# Second child class using super() to call the parent's constructor
class child1(parent):
    def __init__(self, name, age, year):  # Adding year attribute for the child class
        super().__init__(name, age)  # Call parent's constructor using super()
        self.newyear = year  # Assign newyear to the child object

    def fun(self):  # Custom method to print child and parent attributes
        print(self.firstname, self.myage, self.newyear)


# Creating an object of the second child class
c = child1("xyz", 20, 2025)
c.fun()  # Output: 'xyz 20 2025', using the custom method in child class
