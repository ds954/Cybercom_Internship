
from scipy.interpolate import Rbf, UnivariateSpline, interp1d
import numpy as np

# Define the input data
xs = np.arange(10)  # x-values: [0, 1, 2, ..., 9]
ys =  2*xs  # y-values: a function of x

# Create a Linear Interpolation
interp_func_linear = interp1d(xs, ys)

# Interpolate new points using the Linear Interpolation method
newarr_linear = interp_func_linear(np.arange(2.1, 3, 0.1))  # x-values: [2.1, 2.2, ..., 2.9]
print("\nLinear Interpolation Results:")
print(newarr_linear)


# Create a Univariate Spline Interpolation
interp_func_spline = UnivariateSpline(xs, ys)

# Interpolate new points using the UnivariateSpline method
newarr_spline = interp_func_spline(np.arange(2.1, 3, 0.1))  # x-values: [2.1, 2.2, ..., 2.9]
print("\nUnivariate Spline Interpolation Results:")
print(newarr_spline)


# Create a Radial Basis Function Interpolation
interp_func_rbf = Rbf(xs, ys)

# Interpolate new points using the Rbf method
newarr_rbf = interp_func_rbf(np.arange(2.1, 3, 0.1))  # x-values: [2.1, 2.2, ..., 2.9]
print("\nRbf Interpolation Results:")
print(newarr_rbf)


