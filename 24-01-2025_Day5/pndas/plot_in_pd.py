import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\dsm95\Desktop\Cybercom_Internship\24-01-2025_Day5\pndas\data.csv")

df.plot()

df.plot(kind = 'scatter', x = 'Duration', y = 'Calories')
df["Duration"].plot(kind = 'hist')
plt.show()