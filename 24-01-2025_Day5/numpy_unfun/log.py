import numpy as np
from math import log

log_value=np.arange(1,10)
print("log base 2:\n",np.log2(log_value))
print("\nlog base 10:\n",np.log10(log_value))
print("\nlog base e:\n",np.log(log_value))


print("\nfor log at any base:")

nplog = np.frompyfunc(log, 2, 1)

print(nplog(50, 41))