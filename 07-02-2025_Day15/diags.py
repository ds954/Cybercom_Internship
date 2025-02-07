from scipy.sparse import spdiags
import numpy as np

data=np.array([[1,2,3],[8,5,2],[7,9,3]])
diags=np.array([-1,0,2])

matrix=spdiags(data,diags,5,5).toarray()
print(matrix)