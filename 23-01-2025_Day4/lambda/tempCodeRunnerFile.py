import numpy as np

str= "banana"

# Using lambda function to print each character on a new line
# for char in str:
#     (lambda x: print(x))(char)

[lambda x: print(x)(char) for char in str ]