class ProtectedExample:
    def __init__(self):
        self._name = "Protected Member"  # Protected attribute

    def _greet(self):  # Protected method
        return f"Hello, {self._name}"


class SubClass(ProtectedExample):
    def access_protected(self):
        # Accessing the protected member from a subclass
        return self._greet()


# Accessing protected members
obj = SubClass()
print(obj.access_protected())  # Output: Hello, Protected Member
print(obj._name)  # Output: Protected Member
