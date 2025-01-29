from protected1 import _protected_parent,_child


class _newchild(_child):
    def _callNewChild(self):
        print("this is new child")

newchild_obj = _newchild()
newchild_obj._callparent()