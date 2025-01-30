import pandas as pd

data={
    "Name":["Alice","Bob","Charlie"],
    "Age":[25,30,28],
    "Department":["HR","IT","Finance"]
}
df=pd.DataFrame(data)
save_file=df.to_csv("employess.csv",index=False)