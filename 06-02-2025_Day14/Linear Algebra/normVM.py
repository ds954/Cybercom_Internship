from scipy.linalg import norm,svd
import numpy as np

# The norm of a vector or matrix is a measure of its "size" or "magnitude."
a=np.array([-10,2,4,4,5,6,7,8,9])
b=a.reshape((3,3))
print(b)

print("norm of a: ",norm(a))      #sqrt(sum(x_i^2)) root of 285
print("norm of b: ",norm(b,'fro'))      #sqrt(sum(sum(a_ij^2))) Frobenius norm of matrix b

print("infinity norm of a: ",norm(a,np.inf))   #max(abs(x_i))
print("infinity norm of b: ",norm(b,np.inf))   #max(sum(abs(a_ij)) for each row)

print("negative infinity of a: ",norm(a,-np.inf))  #min(abs(x_i))
print("negative infinity norm of b: ",norm(b,-np.inf))   #min(sum(abs(a_ij)) for each row)

print("norm(a, 1):", norm(a, 1)) #sum(abs(a))
print("norm(b, 1):", norm(b, 1)) #max(sum(abs(b), axis=0 column))

print("norm(a, -1):", norm(a, -1))  #sum(abs(a)**ord)**(1./ord)
print("norm(b, -1):", norm(b, -1)) #min(sum(abs(b), axis=0))

print("norm(a, 2):", norm(a, 2))  #sum(abs(a)**ord)**(1./ord)
print("norm(b, 2):", norm(b, 2))  #2-norm (largest sing. value)

# 1/100 + 1/4 + 1/16 + 1/16 + 1/25 + 1/36 + 1/49 + 1/64 + 1/81 = 0.5056
# (0.5056)**(-1/2) = 1.41
print("norm(a, -2):", norm(a, -2))  #sum(abs(a)**ord)**(1./ord)
print("norm(b, -2):", norm(b, -2))  #smallest singular value

U,S,V=svd(b)
print(S)


