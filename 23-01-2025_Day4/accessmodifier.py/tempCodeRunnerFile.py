class _protected_parent:

    def _callparent(self):
        print("this is parent class")


class _child(_protected_parent):
    def _callChild(self):
        print("this is child class")



class __newchild(_child):
    def __callNewChild(self):
        print("this is new child")

newchild_obj = __newchild()
newchild_obj._callparent()