from scipy.cluster.hierarchy import cophenet,single
from scipy.spatial.distance import pdist,squareform

X = [[0, 0], [0, 1], [1, 0],
     [0, 4], [0, 3], [1, 4],
     [4, 0], [3, 0], [4, 1],
     [4, 4], [3, 4], [4, 3]]
Z = single(pdist(X))
cophenet(Z)
squared_form=squareform(cophenet(Z))
print(squared_form)