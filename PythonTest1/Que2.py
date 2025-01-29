# Create a program which uses a function as a parameter in another fucntion.

import pandas as pd

def another_fun(x):
    return x**2

data={
    "col1":[1,2,3],
    "col2":[7,8,9]
}
df=pd.DataFrame(data)
ans=df.apply(another_fun)
print(ans)