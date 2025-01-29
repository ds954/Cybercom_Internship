import numpy as np


arr = np.array([3.14159, -2.71828, 1.61803, -1.23456, 9.87654])

# Truncation (removes the decimal part)
truncation = np.trunc(arr)

# Fix (round towards zero)
fix = np.fix(arr)

# Rounding (nearest integer or decimal places)
rounding = np.round(arr, 2)  # Round to 2 decimal places
rounding_default = np.round(arr)  # Round to nearest integer

# Floor (round down to nearest integer)
floor = np.floor(arr)

# Ceil (round up to nearest integer)
ceil = np.ceil(arr)


print("Original Array:", arr)
print("Truncation:", truncation)
print("Fix (round towards zero):", fix)
print("Rounding (to 2 decimal places):", rounding)
print("Rounding (nearest integer):", rounding_default)
print("Floor (round down):", floor)
print("Ceil (round up):", ceil)
