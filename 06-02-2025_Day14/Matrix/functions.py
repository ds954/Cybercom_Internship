import numpy as np
from scipy.linalg import (
    expm, logm, cosm, sinm, tanm, coshm, sinhm, tanhm, signm, sqrtm, funm,
    expm_frechet, expm_cond, fractional_matrix_power,
    solve_sylvester, solve_continuous_are, solve_discrete_are,
    solve_continuous_lyapunov, solve_discrete_lyapunov
)

# Define a sample matrix A
A = np.array([[0, 1], [-1, 0]])

print("Matrix A:\n", A)
print("\nMatrix Exponential of A:\n", expm(A))
print("\nMatrix Logarithm of expm(A) (should return A):\n", logm(expm(A)))

# Matrix trigonometric functions
print("\nMatrix Cosine of A:\n", cosm(A))
print("\nMatrix Sine of A:\n", sinm(A))
print("\nMatrix Tangent of A:\n", tanm(A))

# Matrix hyperbolic functions
print("\nHyperbolic Cosine of A:\n", coshm(A))
print("\nHyperbolic Sine of A:\n", sinhm(A))
print("\nHyperbolic Tangent of A:\n", tanhm(A))

# Matrix square root and fractional power
print("\nMatrix Square Root of A:\n", sqrtm(A))
print("\nA^0.5 (Fractional Power of A):\n", fractional_matrix_power(A, 0.5))

# Solve Sylvester equation AX + XB = Q
A1 = np.array([[1, 2], [3, 4]])
B1 = np.array([[5, 6], [7, 8]])
Q1 = np.array([[9, 10], [11, 12]])

X_sylvester = solve_sylvester(A1, B1, Q1)
print("\nSolution to Sylvester Equation:\n", X_sylvester)

# Solve Continuous-Time Algebraic Riccati Equation (CARE)
A2 = np.array([[0, 1], [-2, -3]])
B2 = np.array([[0], [1]])
Q2 = np.eye(2)
R2 = np.eye(1)

X_care = solve_continuous_are(A2, B2, Q2, R2)
print("\nSolution to Continuous ARE:\n", X_care)

# Solve Discrete-Time Algebraic Riccati Equation (DARE)
X_dare = solve_discrete_are(A2, B2, Q2, R2)
print("\nSolution to Discrete ARE:\n", X_dare)

# Solve Continuous Lyapunov Equation
A3 = np.array([[0, 1], [-1, -2]])
Q3 = np.eye(2)

X_lyap_cont = solve_continuous_lyapunov(A3, Q3)
print("\nSolution to Continuous Lyapunov Equation:\n", X_lyap_cont)

# Solve Discrete Lyapunov Equation
A4 = np.array([[0.5, 0.1], [0.2, 0.7]])
Q4 = np.array([[1, 0], [0, 1]])

X_lyap_disc = solve_discrete_lyapunov(A4, Q4)
print("\nSolution to Discrete Lyapunov Equation:\n", X_lyap_disc)