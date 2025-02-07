import scipy as sp
import numpy as np

rng = np.random.default_rng()
S = sp.sparse.random(3, 4, density=0, rng=rng)
print(S)