from scipy.sparse import coo_matrix, hstack,vstack

A = coo_matrix([[1, 2], [3, 4]])
B = coo_matrix([[5], [6]])
print(hstack([A,B]).toarray())

A = coo_matrix([[1, 2], [3, 4]])
B = coo_matrix([[5,6]])
print(vstack([A,B]).toarray())