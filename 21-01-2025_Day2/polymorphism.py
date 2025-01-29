# it means "many forms"

#Base class for vehivle
class vehicle:
    # Constructor to initialize brand and color of the vehicle
    def __init__(self,brand,color):
        self.brandname=brand
        self.colorname=color

    # Method to represent movement of the vehicle (default behavior)
    def move(self):
        print('move')
        
#Derived class for car, inheriting from vehicle
class car(vehicle):
    def move(self):
        print("drive")

# Derived class for boat, inheriting from vehicle
class boat(vehicle):
    def move(self):
        print('sail')

# Derived class for plane, inheriting from vehicle
class plane(vehicle):
    pass

# Creating objects of the respective classes
mycar=car('bmw','black')
myboat=boat('Touring 20','grey')
myplan=plane('abc','white')

# Loop through all objects and print their brand, color, and movement
for x in(mycar,myboat,myplan):
    print(x.brandname)
    print(x.colorname)
    x.move()