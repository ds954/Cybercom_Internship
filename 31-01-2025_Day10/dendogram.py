from scipy.cluster.hierarchy import leaves_list,to_tree,ward,dendrogram
from scipy.spatial.distance import pdist
from matplotlib import pyplot as plt
import numpy as np

# Create a linkage matrix (valid linkage)
X = [[0, 0], [0, 1], [1, 0],
     [0, 4], [0, 3], [1, 4],
     [4, 0], [3, 0], [4, 1],
     [4, 4], [3, 4], [4, 3]]
Z = ward(pdist(X))
# print(Z)
tree = to_tree(Z)

# Let's check the count of leaf nodes below the root of the tree
print("Number of leaf nodes under root node:", tree.get_count())
print(tree.get_id())

ans=leaves_list(Z)
# print(ans)
fig = plt.figure(figsize=(7, 5))
dn = dendrogram(Z)
plt.show()