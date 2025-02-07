from scipy.sparse import triu,csr_array

A = csr_array([[1, 2, 0, 0, 3], 
               [4, 5, 0, 6, 7], 
               [3, 4, 8, 9, 0]])
print(A)
print(A.toarray())
print(triu(A).toarray())
print(triu(A).nnz)
print(triu(A,k=-1).toarray())

