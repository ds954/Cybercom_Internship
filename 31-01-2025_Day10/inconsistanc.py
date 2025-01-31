from scipy.cluster.hierarchy import inconsistent, single, maxinconsts, maxdists, maxRstat, to_mlab_linkage, is_valid_im, is_valid_linkage
from scipy.spatial.distance import pdist

X = [[0, 0], [0, 1], [1, 0],
     [0, 4], [0, 3], [1, 4],
     [4, 0], [3, 0], [4, 1],
     [4, 4], [3, 4], [4, 3]]

# Calculate the pairwise distances between the points in X using Euclidean distance (default).
distance_matrix = pdist(X)

# Perform single linkage hierarchical clustering.
# Single linkage uses the minimum distance between clusters to merge them.
# Z is the linkage matrix, which encodes the hierarchical clustering structure.
Z = single(distance_matrix)

# Check if the linkage matrix Z is valid.
print(is_valid_linkage(Z))  # Output: True

# Convert the linkage matrix Z to a MATLAB-style linkage matrix.
# This is useful if you need to use the linkage matrix in MATLAB.
mZ = to_mlab_linkage(Z)
print(mZ)

# Print the linkage matrix Z.
print(Z)

# Calculate the inconsistency coefficients for the linkage matrix Z.
# Inconsistency measures the difference between the height of a link and the 
# average height of the links below it in the dendrogram.
R = inconsistent(Z)
print(inconsistent(Z))

# Find the maximum inconsistency coefficient for each cluster.
# This can be used to identify clusters that are poorly formed or contain outliers.
print(maxinconsts(Z, R))

# Find the maximum distance between any two points within each cluster.
print(maxdists(Z))

# Calculate the maximum R statistic for each cluster.
# The R statistic is a measure of how well a cluster is separated from other clusters.
print(maxRstat(Z, R, 0)) #0 is the column representing the inconsistent statistic

# Check if the inconsistency matrix R is a valid inconsistency matrix.
print(is_valid_im(R))  # Output: True

