import pandas as pd
import numpy as np


def demonstrate_add():
    data = {
        "points": [100, 120, 114],
        "total": [350, 340, 402]
    }
    df = pd.DataFrame(data)
    
    # Add 15 to every element in the DataFrame
    print("Adding 15 to all elements:")
    print(df.add(15))
    
    # Add prefix to column names
    newdf_pre = df.add_prefix("New_")
    print("\nDataFrame with added prefix:")
    print(newdf_pre)
    
    # Add suffix to column names
    newdf_suff = df.add_suffix("_after")
    print("\nDataFrame with added suffix:")
    print(newdf_suff)

# demonstrate_add()

# Function to demonstrate aggregation methods
def demonstrate_agg():
    data = {
        "x": [[50, 40, 30],[1,2,3]],
        "y": [[300, 12, 42],[7,8,9]]
    }
    df = pd.DataFrame(data)
    
    # Aggregate sum of each column
    x = df.agg(["sum"],axis=1)
    print("\nAggregated sum of columns:")
    print(x)
# demonstrate_agg()

# Function to demonstrate the `all` and `any` methods
def demonstrate_all_any():
    data = [[True, False, True], 
            [True, True, True]]
    df = pd.DataFrame(data)
    
    # Check if all values are True in each column
    print("\nAre all values True in each column?")
    print(df.all())
    
    # Check if any value is True in each column
    print("\nAre there any True values in each column?")
    print(df.any())
# demonstrate_all_any()

# Function to demonstrate concatenation of DataFrames
def demonstrate_concat():
    data1 = {
        "age": [16, 14, 10],
        "qualified": [True, True, True]
    }
    df1 = pd.DataFrame(data1)

    data2 = {
        "age": [55, 40],
        "qualified": [True, False]
    }
    df2 = pd.DataFrame(data2)
    
    # Concatenate DataFrames
    newdf = pd.concat([df1, df2], ignore_index=True)
    print("\nConcatenated DataFrame:")
    print(newdf)
# demonstrate_concat()


# Function to demonstrate applymap
def demonstrate_applymap():
    def make_big(x):
       return x.upper() 
    data = {
        "name": ["Sally", "Mary", "John"],
        "city": ["London", "Tokyo", "Madrid"]
    }
    load_csv=pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\27-01-2025_Day6\data2.csv")
    
    df = pd.DataFrame(load_csv)
    
    # Apply `make_big` function to every element of the DataFrame
    newdf = df.applymap(make_big)
    newdf.columns = [col.upper() for col in newdf.columns]
    # print(newdf.columns)
    print("\nDataFrame after applying make_big:")
    print(newdf)
# demonstrate_applymap()

def demonstrate_apply():
    def cum_sum(x):
        return x.cumsum()

    data={
        "A":[12,8,10],
        "B":[10,20,30]
    }
    df=pd.DataFrame(data)
    result1=df.apply(cum_sum,result_type='expand')
    result2=df.apply(cum_sum,result_type='broadcast')
    result3=df.apply(cum_sum,result_type='reduce')

    # print(type(result))
    print(result1)
    print(result2)
    print(result3)
# demonstrate_apply()

def demonstrate_assign():
    # data={
    #     "name":["abc","def","xyz"],
    #     "age":[12,18,20]
    # }
    newdata=[[1,2,3,4],
             [5,6,7,8]]
    # df=pd.DataFrame(newdata)
    # result=df.assign(country=['india','china','nepal'])
    df1=pd.DataFrame(newdata)
    new_result=df1.assign(new_data=[11,12],new_data2=[13, 14])
    print(new_result)
    # print(result)
# demonstrate_assign()

def demonstrate_astype():
    data={
        "col1":[21,22,23],
        "col2":[31.12,32.5,33.7]
    }
    df=pd.DataFrame(data)
    df["col2"] = df["col2"].astype("string")
    result=df.astype("string")
    print_type=df["col2"].dtype
    print(print_type)
    print(result)

    get_value=df.at[2,"col1"]
    print(get_value)

# demonstrate_astype()
   


