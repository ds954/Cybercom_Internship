# Write a function solve_linear_system(coeff_matrix, const_matrix) that solves a linear system of equations using scipy.linalg.solve.

import scipy.linalg as ln
import numpy as np

def solve_linear_system(coeff_matrix, const_matrix):
    return ln.solve(coeff_matrix,const_matrix)

coeff_matrix=np.array([[1,2],
                       [1,1]])
const_matrix=np.array([8,5])
result=solve_linear_system(coeff_matrix,const_matrix)
print(result)
