import pandas as pd

dict1={'A':[12,13,14],
       'B':[1,2,3],
       'C':[10,9,8]}
df=pd.DataFrame(dict1)
print(df)


print(df.loc[0]) #return series
print(df.loc[[0]]) # return dataframe
