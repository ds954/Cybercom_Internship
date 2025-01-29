# Create two DataFrames df1 and df2, Write a Pandas Program to merge them on a common column named "ID".
import pandas as pd

data1={
    "Name":["ABC","DEF","XYZ"],
    "id":[121,122,123]
}

data2={
    "clg":["vgec","LD","Nirma","MSU"],
    "id":[121,122,123,124],
    "Age":[20,21,19,15]
}

df1=pd.DataFrame(data1)
df2=pd.DataFrame(data2)

using_join=df1.set_index("id").join(df2.set_index("id"),how="inner",lsuffix="_left",rsuffix="_right")
print(using_join)