import pandas as pd

lst = [1, 7, 2]

myvar = pd.Series(lst, index = ["x", "y", "z"])

print(myvar)
print(myvar["z"])

dict1={'A':12,
       'B':13,
       'C':14}
result=pd.Series(dict1,index=['A','B'])
print(result)

