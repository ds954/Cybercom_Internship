import pandas as pd 
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age":[15,80,25,60],
    "Salary": [90000, 60000, 70000, 80000],
    "Department": ["HR", "IT", "Finance", "IT"]
    }
df = pd.DataFrame(data)
age_condition = df[["Age"]].le(30)
# print(age_condition.values)
filtered_values = df[df["Age"].le(30)]["Age"].values
print(filtered_values)
# Count the number of True values
count = age_condition.sum()
print(count)
   