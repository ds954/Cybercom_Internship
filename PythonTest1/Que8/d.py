# Write a Pandas program to save the DataFrame as a CSV file named "employees.csv".
import pandas as pd

data={
    "Name":["Alice","Bob","Charlie"],
    "Age":[25,30,28],
    "Department":["HR","IT","Finance"]
}
df=pd.DataFrame(data)

save_file=df.to_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\PythonTest1.py\Que8\employess.csv")
