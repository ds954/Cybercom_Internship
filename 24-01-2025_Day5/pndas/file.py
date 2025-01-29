import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")

# Set the maximum number of rows to display to 170
pd.options.display.max_rows = 170

# Display the first 5 rows of the DataFrame
print("First 5 rows of the dataset:")
print(df.head())

# Display the last 5 rows of the DataFrame
print("\nLast 5 rows of the dataset:")
print(df.tail())

# Display information about the DataFrame (columns, data types, non-null values, etc.)
print("\nInformation about the dataset:")
print(df.info())
