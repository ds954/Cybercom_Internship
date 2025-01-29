# Create a function to return the given number rounded to two decimal places. 
import pandas as pd

def round_fun():
    data={
        "Number":[3.14578,8.12345]
    }
    df=pd.DataFrame(data)
    print(df.round(2))
round_fun()