import numpy as np
from scipy.stats import ttest_ind

v1 = np.random.normal(size=100)
v2 = np.random.poisson(size=100)

res = ttest_ind(v1, v2)

print(res)
res = ttest_ind(v1, v2).pvalue

print(res)