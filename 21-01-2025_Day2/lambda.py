# lambda function can take any number of arguments, but can only have one expression.
# small anonymous function

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
print(mydoubler(11))

# with map()
num=[2,5,9,7]
x=map(lambda i:i**2,num)
print(list(x))

#filter():
num=[2,5,6,8,9]
x=filter(lambda i:i%2==0,num)
print(x)
print(list(x))

#sorted()
words = ["apple", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words) 
  