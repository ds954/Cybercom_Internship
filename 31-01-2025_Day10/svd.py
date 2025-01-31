from scipy import linalg
import numpy as np

arr=np.array([[1,1],
              [7,7]])
U,S,V=linalg.svd(arr)
print("left singular vector:")
print(U)
print("singular value")
print(S)
print("right singular vector:")
print(V)