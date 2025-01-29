class PrivateExample:
    def __init__(self):
        self.__name = "Private Member"  # Private attribute

    def __greet(self):  # Private method
        return f"Hello, {self.__name}"

    def access_private(self):  # Public method to access private members
        return self.__greet()


# Accessing private members
obj = PrivateExample()

# Access through a public method
print(obj.access_private())  # Output: Hello, Private Member

# Direct access will raise an AttributeError
# print(obj.__name)  # AttributeError
# print(obj.__greet())  # AttributeError


print(obj._PrivateExample__name)  # Output: Private Member
print(obj._PrivateExample__greet())  # Output: Hello, Private Member
