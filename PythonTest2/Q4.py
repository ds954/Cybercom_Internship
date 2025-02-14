# What is __init__()? Provide usage with the example.

'''
 when a object of class is created it is automatically called,
 to initialize the atribute of object
'''
class Car:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model
    def display_info(self):
        print("brand name:",self.brand)
        print("model name:",self.model)
    
obj=Car("abc","def")
obj.display_info()