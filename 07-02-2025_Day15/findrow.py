from scipy.sparse import csr_matrix,find


matrix=csr_matrix([[1,2,3],[8,9,6]])
print(find(matrix))
