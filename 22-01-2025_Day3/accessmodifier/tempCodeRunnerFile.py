class PrivateExample:
    def __init__(self):
        self.__name = "Private Member"  # Private attribute

    def __greet(self):  # Private method
        return f"Hello, {self.__name}"

   


# Accessing private members
obj = PrivateExample()



# Direct access will raise an AttributeError
# print(obj.__name)  # AttributeError
# print(obj.__greet())  # AttributeError

# Access using name mangling
print(obj._PrivateExample__name)  # Output: Private Member
print(obj._PrivateExample__greet())  # Output: Hello, Private Member
