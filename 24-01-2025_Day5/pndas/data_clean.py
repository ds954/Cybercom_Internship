import pandas as pd

df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
print("Original DataFrame:")
print(df)

# Drop rows with missing values (does not modify the original DataFrame)
new_df = df.dropna()
print("DataFrame after dropping rows with missing values (without modifying the original):")
print(new_df)

# Drop rows with missing values and modify the original DataFrame
df.dropna(inplace=True)
print("DataFrame after dropping rows with missing values (modifies the original):")
print(df)

# Fill all missing values in the DataFrame with a specific value (e.g., 12)
df.fillna(12)
print("DataFrame after filling all missing values with 12:")
print(df)

# Fill missing values in a specific column (e.g., "Pulse") with a specific value (e.g., 12)
df["Pulse"].fillna(12)
print("DataFrame after filling missing values in the 'Pulse' column with 12:")
print(df)





