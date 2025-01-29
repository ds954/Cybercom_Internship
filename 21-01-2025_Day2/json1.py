#storing and exchanging data.

#json to python
import json
x='{"name":"abc","age":25}'
y=json.loads(x)
print(y)#return dict

#python to json
x={"name":"abc","age":25}
y=json.dumps(x) #return json
print(y)

import json

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

# sort the result alphabetically by keys:
print(json.dumps(x, sort_keys=True)) # specify if the result should be sorted or not: