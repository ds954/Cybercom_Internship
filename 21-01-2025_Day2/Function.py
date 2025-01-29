#Arbitary argument *arg

def fun(*fruit):
    print(fruit[1])

fun("apple","banana")


#Arbitary argument **kewargs
def fun1(**color):
    print(color['c2'])
fun1(c1='red',c2='green')

#Default Parameter Value
def my_function(country = "Norway"):
  print("I am from " + country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")

#list as an argument
def colorfun(color):
   for x in color:
      print(x)

color=['red','green','yellow']
colorfun(color)

#positional only argument:
def fun(x,/):
   print(x)
fun(25)

#keyword only argument:
def fun(*,x):
   print(x)
fun(x=25)

#positional only and keyword only argument:
def my_function(a, b, /, *, c, d):
  print(a + b + c + d)

my_function(5, 6, c = 7, d = 8)
