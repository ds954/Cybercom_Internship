import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
print("Original DataFrame:")
print(df)

# Calculate the mean of the "Calories" column and fill missing values with it
mean_val = df["Calories"].mean()
df["Calories"].fillna(mean_val, inplace=True)
print("DataFrame after filling missing values in the 'Calories' column with the mean value:")
print(df)

#  Calculate the median of the "Calories" column and fill missing values with it
median_val = df["Calories"].median()
df["Calories"].fillna(median_val)
print("DataFrame after filling missing values in the 'Calories' column with the median value:")
print(df)

# Calculate the mode of the "Calories" column and fill missing values with it
mode_val = df["Calories"].mode()[0]
df["Calories"].fillna(mode_val)
print("DataFrame after filling missing values in the 'Calories' column with the mode value:")
print(df)