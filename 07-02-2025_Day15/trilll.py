from scipy.sparse import tril,csr_array

A = csr_array([[1, 2, 0, 0, 3], 
               [4, 5, 0, 6, 7], 
               [3, 4, 8, 9, 0]])
print(A)
print(A.toarray())
print(tril(A).toarray())
print(tril(A).nnz)
print(tril(A,k=-1).toarray())
print(tril(A,k=2).toarray())
