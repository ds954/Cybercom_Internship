import pandas as pd 
import numpy as np
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Bonus": [1500, 2500, 1500,5000],
    "Age":[15,80,15,60],
    "Salary": [90000, 50000, 70000, 80000],
    "Department": ["HR", "IT", "Finance", "IT"]
}
df = pd.DataFrame(data)
df[:]=np.nan
df.columns=[np.nan]*df.shape[1]
df.index=[np.nan]*df.shape[0]
print(df)