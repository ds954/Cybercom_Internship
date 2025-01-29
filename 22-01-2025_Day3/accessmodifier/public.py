class PublicExample:
    def __init__(self):
        self.name = "Public Member"  # Public attribute

    def greet(self):  # Public method
        return f"Hello, {self.name}"


# Accessing public members
obj = PublicExample()
print(obj.name)  # Output: Public Member
print(obj.greet())  # Output: Hello, Public Member
