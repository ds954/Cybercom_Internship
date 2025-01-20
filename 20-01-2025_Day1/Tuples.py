#Tuple items are ordered, unchangeable, and allow duplicate values.

#To add a iteam in tuple convert it into a list then add and again convert it into tuple or by following method:
thistuple = ("apple", "banana", "cherry")
y = ("orange",)
thistuple += y
print(thistuple)

#join tuple
tuple1=(1,2,3)
tuple2=("x","y","z")
print(tuple1+tuple2)

#unpack tuple
thistuple = ("apple", "banana", "cherry","blueberry","strawberry","orange")
x,*y,z=thistuple #fist and last value assign to the x and z and remaining assign to the y as a list
print(x)
print(y)
print(z)
