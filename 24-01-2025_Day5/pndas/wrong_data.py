import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
print("Original DataFrame:")
print(df)

# Replace values in the "Duration" column greater than 100 with 100
for x in df.index:
    if df.loc[x, "Duration"] > 100:
        df.loc[x, "Duration"] = 100
print("\nDataFrame after capping 'Duration' values at 100:")
print(df)

# Identify duplicated rows in the DataFrame
x = df.duplicated()

# Display only the rows that are duplicates
print("\nDuplicated rows:")
print(df.loc[x])

# Drop all duplicate rows in the DataFrame (in-place modification)
df.drop_duplicates()

# Get the indices of the duplicated rows
duplicated_indices = df.index[x]  # This will contain indices of rows that were marked as duplicates

# Print the indices of duplicated rows
print("\nIndices of duplicated rows:")
print(duplicated_indices)

print(df.corr())

