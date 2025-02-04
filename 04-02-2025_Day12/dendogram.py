import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, single
from scipy.spatial.distance import pdist

# Your data points
X = [[0, 0], [0, 1], [1, 0],
     [0, 4], [0, 3], [1, 4],
     [4, 0], [3, 0], [4, 1],
     [4, 4], [3, 4], [4, 3]]

# Calculate the pairwise distances between the points using Euclidean distance
distance_matrix = pdist(X)

# Perform single linkage hierarchical clustering
Z = single(distance_matrix)

# Create and display the dendrogram
plt.figure(figsize=(10, 6))
dendrogram(Z)
plt.title("Dendrogram of Single Linkage Hierarchical Clustering")
plt.xlabel("Index of Points")
plt.ylabel("Distance")
plt.show()
