import numpy as np

str= "banana"
print("method 1:")
for char in str:
    (lambda x: print(x))(char)

print("\nmethod 2:")
[(lambda x: print(x))(char) for char in str ]


print("\nmethod 3:")

# Using map with lambda to print each character
list(map(lambda x: print(x), str))

