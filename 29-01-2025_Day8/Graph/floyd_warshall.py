import numpy as np
from scipy.sparse.csgraph import floyd_warshall
from scipy.sparse import csr_matrix

# Adjacency matrix
arr = np.array([
  [0, 3, 8, np.inf],
  [np.inf, 0, np.inf, 1],
  [np.inf, 4, 0, 2],
  [np.inf, np.inf, 5, 0]
])

# Convert to sparse matrix
newarr = csr_matrix(arr)

# Apply Floyd-Warshall algorithm
dist_matrix, pred_matrix = floyd_warshall(newarr, return_predecessors=True)

# Print results
print("Shortest path distance matrix:")
print(dist_matrix)

print("\nPredecessor matrix:")
print(pred_matrix)
