import numpy as np
from scipy.stats import describe,skew, kurtosis,normaltest

v = np.random.normal(size=100)
res = describe(v)

print(res)
print(skew(v))
print(kurtosis(v))
print(normaltest(v))