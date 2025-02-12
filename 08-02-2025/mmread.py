from io import StringIO
from scipy.io import mmread

text = '''%%MatrixMarket matrix coordinate real general
 5 5 7
 2 3 1.0
 3 4 2.0
 3 5 3.0
 4 1 4.0
 4 2 5.0
 4 3 6.0
 4 4 7.0
'''

m = mmread(StringIO(text), spmatrix=False) #returns the data as sparse array in COO format.
print(m)
print(m.toarray())