import pandas as pd
import numpy as np

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Bonus": [1500, 2500, 1500,5000],
    "Age":[15,80,15,60],
    "Salary": [90000, 50000, 70000, 80000],
    "Department": ["HR", "IT", "Finance", "IT"]
}
df = pd.DataFrame(data)


def demonstrate_join():
    df_other = pd.DataFrame({"Department": ["HR", "IT","Bio"], 
                             "Bonus": [1000, 2000,3000]})
    # print(df.set_index("Department").join(df_other.set_index("Department"),how='inner',lsuffix="_left", rsuffix="_right"))
    # print(df.set_index("Department").join(df_other.set_index("Department"),how='left',lsuffix="_left", rsuffix="_right"))
    print(df.set_index("Department").join(df_other.set_index("Department"),how='right',lsuffix="_left", rsuffix="_right"))
    # print(df.set_index("Department").join(df_other.set_index("Department"),how='outer',lsuffix="_left", rsuffix="_right"))
# demonstrate_join()

def demonstrate_last():
    df_time = pd.DataFrame({
        "Value": [10, 20, 30],
        "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"])
    }).set_index("Date")
    print(df_time.last("2D"))
# demonstrate_last()

def demonstrate_le():
    data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age":[15,80,25,60],
    "Salary": [90000, 60000, 70000, 80000],
    "Department": ["HR", "IT", "Finance", "IT"]
    }
    df = pd.DataFrame(data)
    print(df[["Age"]].le(30))
# demonstrate_le()

def demonstrate_loc():
    print(df)
    print(df.loc[1:3, ["Name", "Age"]])
# demonstrate_loc()

def demonstrate_lt():
    print(df[["Salary"]].lt(60000,axis=1))
# demonstrate_lt()

def demonstrate_keys():
    print(df.keys())
# demonstrate_keys()

def demonstrate_mask():
    print(df.mask(df))
# demonstrate_mask()

def demonstrate_max():
    print(df.max())
# demonstrate_max()

def demonstrate_mean():
    print(df.mean(numeric_only=True))
# demonstrate_mean()

def demonstrate_median():
    print(df.median(numeric_only=True))
# demonstrate_median()

def demonstrate_melt():
    print(pd.melt(df, id_vars=["Name","Bonus"], value_vars=["Age", "Salary"]))
    #long table with one row for each each column.
    # df=pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    # print(df.melt())
# demonstrate_melt()

def demonstrate_memory_usage():
    # df=pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    print(df.memory_usage())
# demonstrate_memory_usage()

def demonstrate_merge():
    df_other = pd.DataFrame({"Department": ["HR", "IT"], "Bonus": [1000, 2000]})
    print(pd.merge(df, df_other, on="Department", how="left"))
# demonstrate_merge()

def demonstrate_min():
    print(df.min())
# demonstrate_min()

def demonstrate_mod():
    print(df["Age"].mod(5))
# demonstrate_mod()

def demonstrate_mode():
    print(df.mode(numeric_only=True))
# demonstrate_mode()

def demonstrate_mul():
    print(df["Age"].mul(2))
# demonstrate_mul()

def demonstrate_ndim():
    print(df.ndim)
# demonstrate_ndim()

def demonstrate_ne():
    print(df["Department"].ne("IT"))
# demonstrate_ne()

def demonstrate_nlargest():
    print(df.nlargest(2, "Salary"))
# demonstrate_nlargest()

def demonstrate_notna():
    df=pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    print(df.notna()) #replace all values in the DataFrame with True for NOT not-a-number values, otherwise False
# demonstrate_notna()

def demonstrate_notnull():
    df=pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    print(df.notnull())#replace all values in the DataFrame with True for NOT NULL values
# demonstrate_notnull()

def demonstrate_nsmallest():
    print(df.nsmallest(2, "Salary"))#Sort the DataFrame by the specified columns, ascending, and return the specified number of rows
# demonstrate_nsmallest()

def demonstrate_nunique():
    print(df.nunique(axis=1))
# demonstrate_nunique()

def demonstrate_pct_change():
    print(df[["Age", "Salary"]].pct_change())
# demonstrate_pct_change()

def demonstrate_pipe():
    def add_bonus(dataframe):
        dataframe["Bonus"] = dataframe["Salary"] * 0.1
        return dataframe
    
    print(df.pipe(add_bonus))
# demonstrate_pipe()

def demonstrate_pivot():
    df_pivot = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Year": [2022, 2022, 2023],
        "Salary": [50000, 60000, 70000]
    })
    print(df_pivot.pivot(index="Year", columns="Name", values="Salary"))
# demonstrate_pivot()

def demonstrate_pivot_table():
    print(df.pivot_table(values="Salary", index="Department", aggfunc="mean"))
# demonstrate_pivot_table()

def demonstrate_pop():
    df_copy = df.copy()
    print(df_copy.pop("Salary"))
    print(df_copy)
# demonstrate_pop()

def demonstrate_pow():
    print(df[["Age","Salary"]].pow(2))
# demonstrate_pow()

def demonstrate_prod():
    print(df["Age"].prod())
# demonstrate_prod()


def demonstrate_query():
    print(df.query("Age > 30"))
# demonstrate_query()

def demonstrate_radd():
    print(df["Age"].radd(10))
# demonstrate_radd()

def demonstrate_rdiv():
    print(df["Age"].rdiv(100))
# demonstrate_rdiv()

def demonstrate_reindex():
    print(df.reindex([0, 2, 3]))
# demonstrate_reindex()

def demonstrate_rename():
    print(df.rename(columns={"Age": "Years"}))
# demonstrate_rename()

def demonstrate_rename_axis():
    print(df.rename_axis("members"))
# demonstrate_rename_axis()


def demonstrate_replace():
    print("\n39. replace():")
    print(df.replace({"IT": "Tech"}))
# demonstrate_replace()

def demonstrate_reset_index():
    print(df.reset_index(drop=True))
# demonstrate_reset_index()

def demonstrate_sample():
    print(df.sample(2))
# demonstrate_sample()

def demonstrate_sem():
    print("Standard Error of the Mean:")
    print(df.sem(numeric_only=True))
# demonstrate_sem()

# Function to select numeric columns and display them
def demonstrate_select_dtypes():
    print("Selecting Numeric Columns:")
    print(df.select_dtypes(include=['number']))
# demonstrate_select_dtypes()

# Function to display the shape of the DataFrame
def demonstrate_shape():
    print("Shape of the DataFrame:")
    print(df.shape)
# demonstrate_shape()

# Function to set custom axis and display the updated DataFrame
def demonstrate_set_axis():
    df_new_columns = df.set_axis(["Employee_Name", "Employee_Bonus", "Employee_Age", "Employee_Salary", "Employee_Department"], axis=1)
    print("DataFrame with New Column Names:")
    print(df_new_columns)
# demonstrate_set_axis()


def demonstrate_set_index():
    print(df.set_index("Name"))
# demonstrate_set_index()

def demonstrate_size():
    print(df.size)
# demonstrate_size()

def demonstrate_sort_index():
    data={ "Name": ["Alice", "Bob", "Charlie", "David"],
    "Bonus": [1500, 2500, 1500,5000],
    "Age":[15,80,15,60],
    "Salary": [90000, 50000, 70000, 80000],
    "Department": ["HR", "IT", "Finance", "IT"]
    }
    idx=["A","Z","F","Q"]
    df=pd.DataFrame(data,index=idx)
    ans=df.sort_index(ascending=False)
    print(ans)
# demonstrate_sort_index()

def demonstrate_sort_values():
    print(df.sort_values(by="Salary"))
# demonstrate_sort_values()

def demonstrate_squeeze():
    print(df[["Name"]].squeeze())
# demonstrate_squeeze()

def demonstrate_stack():
    print(df.stack())
# demonstrate_stack()

def demonstrate_sum():
    print(df.sum(numeric_only=True))
# demonstrate_sum()

def demonstrate_sub():
    print(df["Age"].sub(5))
# demonstrate_sub()



def demonstrate_T():
    print(df.T)
# demonstrate_T()


def demonstrate_take():
    print(df.take([0, 3]))
# demonstrate_take()



def demonstrate_transform():
    print(df["Age"].transform(lambda x: x * 2))
# demonstrate_transform()

def demonstrate_truncate():
    print(df.truncate(before=1, after=2))
# demonstrate_truncate()

def demonstrate_value_counts():
    print(df["Department"].value_counts())
# demonstrate_value_counts()

def demonstrate_values():
    print(df.values)
# demonstrate_values()


def demonstrate_where():
    print(df.where(df["Age"] > 30))
# demonstrate_where()

def demonstrate_xs():
    df_multi = df.set_index(["Name", "Department"])
    print(df_multi.xs("IT", level="Department"))
# demonstrate_xs()

def demonstrate_iter():
    for col in df.__iter__():
        print(col)
# demonstrate_iter()
