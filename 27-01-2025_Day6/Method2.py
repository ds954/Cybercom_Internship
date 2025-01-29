import pandas as pd
import numpy as np

# Function to read CSV file and display basic information about DataFrame
def read_and_display_csv():
    df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    print("Columns in the DataFrame:")
    print(df.columns)  # Display column names
    print("Axes of the DataFrame:")
    print(df.axes)  # Display axes
    print("Full DataFrame:")
    print(df)  # Display the full DataFrame
    return df

def Manuplate_CSV():
     df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
     print(df.head())
     print(df.axes)
     drop_value=df.dropna()
     print("After Drop a Value:")
     print(drop_value.axes)
# Manuplate_CSV()

# read_and_display_csv()

# Function to handle backfill missing values
def backfill_data():
    df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    newdff = df.bfill()  # Backfill missing values
    print("DataFrame after backfilling missing values:")
    # print(newdff.head())
    print(newdff.tail())
    return newdff
# backfill_data()

# Function to demonstrate combine with a custom function
def combine_with_custom_func():
    df1 = pd.DataFrame([[1, 2], [3, 4]])
    df2 = pd.DataFrame([[5, 6], [7, np.nan]])
    
    # Custom function to compare sum of two DataFrames' columns
    def myfunc(a, b):
        if (a.sum() > b.sum()):
            return a
        else:
            return b

    # Combine df1 and df2 based on the custom function
    combined_df = df1.combine(df2, myfunc, fill_value=45)
    print("DataFrame after combine:")
    print(combined_df)

    # Use combine_first to fill NaN in df2 with values from df1
    combined_first_df = df2.combine_first(df1)
    print("DataFrame after combine_first:")
    print(combined_first_df)
# combine_with_custom_func()

# Function to demonstrate convert_dtypes for dtype conversion
def convert_dtypes_example():
    data = {
        "name": ["Sally", "Mary", pd.NA],
        "qualified": [True, False, pd.NA]
    }
    df = pd.DataFrame(data)

    print("Original dtypes:")
    print(df.dtypes)  # Display original dtypes
    
    # Convert dtypes to the most appropriate type
    newdf = df.convert_dtypes()
    print("New dtypes after conversion:")
    print(newdf.dtypes)  # Display new dtypes
    print("Count non Nan Value:")
    print(df.count())

# convert_dtypes_example()

def demonstarate_Cov():
    data=[[1,2,3],[4,5,6]]
    df = pd.DataFrame(data)
    print(df.cov(min_periods=2,ddof=0))
# demonstarate_Cov()

def demonstrate_copy():
   
    df=pd.DataFrame([5,7,8])
    copy_df=df.copy(deep=True)
    print("original: \n",df)
    copy_df.iloc[1]=9999
    print("copy of df: \n",copy_df)
    print("original: \n",df)
# demonstrate_copy()

def demonstrate_cummax():
    df=pd.DataFrame([[8,3,4],
                     [15,2,78]])
    column_df=df.cummax(axis=0)
    row_df=df.cummax(axis=1)
    print(column_df)
    print(row_df)
    print(df.describe())
# demonstrate_cummax()

def demonstrate_diff():
   data = [[10, 18, 11], [13, 15, 8], [9, 20, 3]]
   df = pd.DataFrame(data)
   print(df.diff())
   print(df.div(5))
# demonstrate_diff()

def demonstrate_dot():
    df=pd.DataFrame([[1,2,3],[4,5,6]])
    df1=pd.DataFrame([[10,20,30],[40,50,60]])
    # [1,2,3] [10,40]  10+40+90=140    40+100+180=320
    # [4,5,6] [20,50]  40+100+180=320   160+250+360=770
    #         [30,60]
    print(df.dot(df1.T))
# demonstrate_dot()

def demonstrate_drop():
    data={
        "Name":["abc","def","xyz"],
        "City":["Dwarka","Rajkot","Baroda"]
    }
    df=pd.DataFrame(data)
    drop_city=df.drop("City",axis='columns',inplace=True)
    print(drop_city)
    print(data)
# demonstrate_drop()

def demonstrate_droplevel():
    df = pd.DataFrame([
    [2, 3, 4, 5],
    [6, 7, 8, 9],
    [10, 11, 12, 13]]).set_index([0, 1])
    newdf=df.droplevel(0)
    print(newdf)

def demonstrate_empty():
    df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")
    print(df.empty)
# demonstrate_empty()

def demonstarte_eq():
    data=pd.DataFrame([[1,2,3],[8,9,12]])
    print(data.eq(12,axis=0))
# demonstarte_eq()

def demonstrate_equals():
    df=pd.DataFrame([[1,2,3],[8,9,12]])
    df1=pd.DataFrame([[1,2,3],[8,9,12]])
    print(df.equals(df1))
    print(df.duplicated(df1,keep='first'))
# demonstrate_equals()


def demonstrate_eval():
    # data={
    #     "A":[1,2,3],
    #     "B":[7,8,9]
    # }
    # df=pd.DataFrame(data)
    # print(df.eval(['A+B']))
    x = 20  
    y = 30  
    expr = 'x + y + z'  
    result = eval(expr, {'x': x, 'y': y}, {'z': 50})  
    print(result)  
# demonstrate_eval()

def demonstrate_filter():
    data = {
    "name": ["Sally", "Mary", "John"],
    "age": [50, 40, 30],
    "qualified": [True, False, False]
    }
    df = pd.DataFrame(data)

    newdf = df.filter(like="age")

    print(newdf)
# demonstrate_filter()

def demonstrate_first():
    data = pd.date_range(start='2021-01-01', end='2021-01-20')
    value = {
    'P': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    }
    df = pd.DataFrame(value, index=data)
    print(df.first('5D'))
# demonstrate_first()

def demonstrate_floordiv():
    data={
        "A":[10.1,10.5,108],
        "B":[15,105,25]
    }
    df=pd.DataFrame(data)
    print(df.floordiv(10))
    print(df.ge(20))
# demonstrate_floordiv()

def demonstrate_get():
    data={
        "A":[10.1,10.5,108],
        "B":[15,105,25]
    }
    df=pd.DataFrame(data)
    print(df.get("B"))
# demonstrate_get()

def demonstrate_groupby():
    data = {
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Grade': ['A', 'B', 'A', 'A', 'B'],
        'Score': [90, 85, 92, 88, 78]
    }

    df = pd.DataFrame(data)
    agg_functions = {
        
        'Score': ['mean', 'max'] 
    }
    grouped = df.groupby(['Gender', 'Grade']).aggregate(agg_functions)
    print(grouped)

# demonstrate_groupby()

