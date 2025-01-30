import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix

arr = np.array([
  [0, 5, 7],
  [8, 0, 0],
  [10, 0, 0] 
 
])

newarr = csr_matrix(arr)

print(dijkstra(newarr, return_predecessors=True, indices=2))