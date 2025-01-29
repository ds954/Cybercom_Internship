# A file containg set of function called module.

import platform
print(platform.system())
print(dir(platform))

#create own module

def mymodule(name):
    print("user: ",name)

person1 = {
  "name": "John",
  "age": 36,
  "country": "Norway"
}
