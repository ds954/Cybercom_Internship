#it means you traverse through values
# contain 2 method iter() and next()
mytuple = ("apple", "banana", "cherry")

# Creating an iterator object from the tuple using iter()
myit = iter(mytuple)

# Using next() to traverse through the values of the iterator
print(next(myit))  # Output: 'apple' (first element)
print(next(myit))  # Output: 'banana' (second element)
print(next(myit))  # Output: 'cherry' (third element)

# Defining a custom iterator class
class iterator:
    def __iter__(self):
        self.a = 1  # Initialize the starting value of the iterator
        return self  # Return the iterator object itself
    
    def __next__(self):
        if self.a <= 10:  # Check if the value is less than or equal to 10
            x = self.a  # Assign the current value to x
            self.a += 1  # Increment the value of a
            return x  # Return the value
        else:
            raise StopIteration  # Raise StopIteration when the value exceeds 10

# Creating an object of the iterator class
obj = iterator()

# Creating an iterator from the object
mynext = iter(obj)

# Using a for loop to iterate through the values using the iterator
for x in mynext:
    print(x)  # This will print values from 1 to 10
