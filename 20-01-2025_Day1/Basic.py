#Python indentation:

#Python use indentation for indicate block of code
for i in range(1,5):
    print(i)


#Comments:

# For Multiline comments we can use multiline string.
"""
This is Multiline Comment 
used in python 
"""
print("Comments")


#Variable:

#Variables are Containers for storing data values.
var1=78
var2='hello'
var3=3.2
print(var1)
print(var2)
print(var3)


#Casting:
x=str(var1)  #convert into string data type:'78'
y=int(var3)  #convert into integer data type:3
print(x)
print(y)


#type():
print(type(x)) 
print(type(y))


#Variable names are case sensitive:

a=5
A=45
#Both have different value and there is no error
print(a) 
print(A)

#Variable Name:

"""
It can be start with underscore or letter and can not start with digit
can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
it is case sensitive
"""
#Multi-word variable name:

#Camel Case:
myVariableName='camel case' #each word, except the first, starts with a capital letter.
#Pascal Case
MyVariableName ='pascal case' #each word starts with a capital letter.
#Snake Case
my_variable_name = 'snake case' #each word is separated by an underscore character.

#Multiple values:
a,b,c= "value1" ,"value2" ,"value3" #Many Values to Multiple Variables
print(a)
print(b)
print(c)

a=b=c="Value" #One value to Multiple variables
print(a)
print(b)
print(c)

#Unpack Value
color=['red','blue','black']
x,y,z=color
print(x,y,z) #output multiple variables which support different data types
print(x+y+z) # can not support different data types

#Global Variables

x="global"

def fun():
    x="local"
    print("inside",x)

fun()
print("outside",x)

def fun1():
    global x #global variable inside function using global keyword
    x="python"

fun1()
print(x)

#Data Types:

#frozenset:
a=frozenset({34,56,78}) #it is immutable set  
print(type(a))

#random():
import random
print(random.randrange(1,10)) #give random value from 1 to 9
