# Write a Pandas program  to add a new column "Salary" with values [50000, 60000, 55000] to the existing DataFrame.
import pandas as pd
data={
    "Name":["Alice","Bob","Charlie"],
    "Age":[25,30,28],
    "Department":["HR","IT","Finance"]
}
df=pd.DataFrame(data)
add_col=df.assign(Salary=[50000,60000,55000])
print("Copy of original")
print(add_col)

#Direct
df["Salary"]=[50000,60000,55000]
print("Change in existing")
print(df)