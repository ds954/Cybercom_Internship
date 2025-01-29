

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