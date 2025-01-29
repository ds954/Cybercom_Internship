import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix


arr = np.array([
  [0, 1, 0, 0],
  [1, 0, 0, 0],
  [0, 0, 0, 1],
  [0, 0, 1, 0]
])

# Convert the adjacency matrix to CSR format
newarr = csr_matrix(arr)
print(newarr)
# Find the connected components
num_components, labels = connected_components(newarr)

# Print the result
print(f"Number of connected components: {num_components}")
print(f"Component labels for each node: {labels}")