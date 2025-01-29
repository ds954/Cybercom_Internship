import pandas as pd

df=pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\PythonTest1.py\winemag-data-130k-v2 (1).csv")
# print(df)
selected_row=df.loc[[1,2,3,5,8]]
print(selected_row)