from scipy.sparse import coo_array, block_array
A = coo_array([[1, 2], [3, 4]])
B = coo_array([[5], [6]])
C = coo_array([[7]])
result=block_array([[A, B], [None, C]])
new_result=block_array([[A, None], [None, C]])
print(result)
print(new_result)