class _protected_parent:

    def _callparent(self):
        print("this is parent class")


class _child(_protected_parent):
    def _callChild(self):
        print("this is child class")