# Write a Pandas program  to sort the DataFrame by Age in descending order.
import pandas as pd
data={
    "Name":["Alice","Bob","Charlie"],
    "Age":[25,30,28],
    "Department":["HR","IT","Finance"]
}
df=pd.DataFrame(data)

df.sort_values(by='Age',ascending=False,inplace=True)
print("sort by age in decending order:")
print(df)

