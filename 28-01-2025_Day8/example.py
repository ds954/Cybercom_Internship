import scipy.datasets
import matplotlib.pyplot as plt
from scipy.differentiate import derivative
from scipy.integrate import quad,dblquad

ascent = scipy.datasets.ascent()
ascent.shape

# ascent.max()
# # plt.gray()
# plt.imshow(ascent) #create image from 2D array
# plt.show()



# Define function
def f(x):
    return x**3 + 2*x**2 - 5*x + 1

# Compute first derivative at x = 2
x0 = 2

first_derivative = derivative(f, x0)

print(f"First derivative at x = {x0} is {first_derivative}")

result = quad(f, 1, 3)

print(f"Definite integral result: {result}")


def f(x, y):
    return x * y

# Compute double integral
result, error = dblquad(f, 0, 2, lambda x: 0, lambda x: x)

print(f"Double Integral result: {result}")
print(f"Estimated error: {error}")