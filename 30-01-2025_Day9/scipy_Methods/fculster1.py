from scipy.cluster.hierarchy import ward, fcluster, fclusterdata, single, complete, average, weighted, centroid, median,cophenet,inconsistent,linkage
from scipy.spatial.distance import pdist

import numpy as np
X = np.array([[1, 2], [2, 3], [3, 3], [8, 8], [8, 9], [25, 80]])
y = pdist(X)
print(y)

def ward_clustering(X, t, criterion='distance'):
    Z = ward(y)
    print(cophenet(Z,y))
    return fcluster(Z, t=t)
# print("Ward Clustering:", ward_clustering(X, t=0.5))

def single_clustering(X, t=1.5, criterion='distance'):
    Z = single(y)
    return fcluster(Z, t=t, criterion=criterion)
# print("Single Clustering:", single_clustering(X, t=1.5))

def complete_clustering(X, t=1.5, criterion='distance'):
    Z = complete(y)
    return fcluster(Z, t=t, criterion=criterion)
# print("Complete Clustering:", complete_clustering(X, t=1.5))

def average_clustering(X, t=1.5, criterion='distance'):
    Z = average(y)
    return fcluster(Z, t=t, criterion=criterion)
# print("Average Clustering:", average_clustering(X, t=1.5))

def weighted_clustering(X, t=1.5, criterion='distance'):
    Z = weighted(y)
    return fcluster(Z, t=t, criterion=criterion)
# print("Weighted Clustering:", weighted_clustering(X, t=1.5))

def centroid_clustering(X, t=1.5, criterion='distance'):
    Z = centroid(y)
    return fcluster(Z, t=t, criterion=criterion)
# print("Centroid Clustering:", centroid_clustering(X, t=1.5))

def median_clustering(X, t=1.5, criterion='distance'):
    Z = median(y)
    return fcluster(Z, t=t, criterion=criterion)
# print("Median Clustering:", median_clustering(X, t=1.5))


