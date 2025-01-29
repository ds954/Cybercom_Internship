import pandas as pd

df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
row1 = df.sample(n = 1) 
print(row1)

# row_25=df.sample(frac=.25)
# print(row_25)
ans=df.isnull()
print(ans)
# ans=df.isna()
# print(ans)
