import pandas as pd
import numpy as np

def demonstrate_iat():
      data = {
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Grade': ['A', 'B', 'A', 'A', 'B'],
        'Score': [90, 85, 92, 88, 78]
    }
      df=pd.DataFrame(data)
      ans=df.iat[0,2] #col,row
      print(ans)
# demonstrate_iat()

def demonstrate_idxmax():
        data = {
        # 'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Total': [500,100,15,85,70],
        'Score': [90, 85, 92, 88, 78]
    }
        df=pd.DataFrame(data)
        print(df.idxmax(axis='columns'))
        print(df.idxmin())
# demonstrate_idxmax()        

def demonstrate_infer_object():
        data = {
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Total': [500,100,15,85,70],
        'Score': [90, 85, 92, 88, 78]
        }
        df = pd.DataFrame(data)

        print("Original DataFrame:")
        print(df)
        print("Original dtypes:")
        print(df.dtypes)

        #Remove the first row in both colums:

        df = df.iloc[1:]

        print("New DataFrame:")
        print(df)

        # newdf = df.convert_dtypes()
        newdf = df.infer_objects()

        print("New dtypes:")
        print(newdf.dtypes)

# demonstrate_infer_object()

def demonstrate_interplot():
    data = {'A': [np.nan,7, 3, np.nan, np.nan]}
    df = pd.DataFrame(data)
    print("Original DataFrame:")
    print(df)

    # Interpolation (linear by default)
    print("\nAfter Interpolation:")
    print(df.interpolate())
    print(df.ffill())
demonstrate_interplot()