#Multiline String

a="""This is 
Multiline String 
in python"""  #three single qoutes are also use
print(a)

print(a[5]) # give 5th index's Character
for i in a:  #Looping through string
    print(i) 
print(len(a)) #return length of string

#check word existance in string using in and not in
print("python" in a) #return boolean value
if "str" not in a:
    print("none") 

#Slicing
print(a[2:]) #from 2nd index to end
print(a[:7]) #from start 6th index
print(a[-4:-1]) #start the slice from the end of the string

#Escape Characters
str = 'It\'s alright.'
print(str) 
str = "This will insert one \\ (backslash)."
print(str)
str= "This will insert \n newline"
print(str)

#Methods in string
x="  Python,Language "
print(x.upper()) #return String in Uppercase 
print(x.lower()) #return string in lowercase
print(x.lstrip()) #remove leftside whitespace
print(x.rstrip()) #remove rightside whitespace
print(x.strip())#remove all space
print(x.replace("a","z"))
print(x.split(","))



var="python is GOOD."
print(var.capitalize()) #First letter is uppercase
print(var.casefold())#return lowercase
print(var.center(25,"o"))#Returns a centered string
print(var.count("O")) #return number of occurence of string
print(var.endswith("is",2,8)) #return true or false
a=var.endswith(("Bad.","GOOD."))
print(a) 
print(var.find("GOOD.",2,15)) #return -1 if not found
print(var.find("bad")) #raise exception if not found

txt = "H\te\tl\tl\to" 
print(txt)
print(txt.expandtabs())
print(txt.expandtabs(2))
print(txt.expandtabs(4))
print(txt.expandtabs(10)) #Tab size (default:8)

#Formating
grade=8
price=80
print(f"i am in {grade} semester")
print(f"The price is {price:.2f} dollars") #fixed point number with 2 decimals
txt="my name is {fname},i am in {num} sem".format(fname='dhara',num=8)
print(txt)
txt="my name is {0},i am in {1} sem".format('dhara',8)
print(txt)
txt="my name is {},i am in {} sem".format('dhara',8)
print(txt)

#join()
lst=["apple","orange","mango"]
joinchar=' is fruit, '
print(joinchar.join(lst))

#ljust()
txt = "python"
x = txt.ljust(20, "o") #Returns a left justified version of the string
print(x)
print(x.count("o"))

#isinstance()
x = 20.25
print(isinstance(x, int)) #return true if x is int

