# Write a Pandas program to replace all missing values (NaN) in a DataFrame with 0.
import pandas as pd

data={
    "Name":["Alice","Bob",pd.NA],
    "Age":[25,30,pd.NA],
    "Department":[pd.NA,"IT","Finance"]
}
df=pd.DataFrame(data)

df.fillna(0,inplace=True)
print(df)