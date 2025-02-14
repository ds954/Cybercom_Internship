# Write a function find_root() that finds the root of the function f(x) = x^3 - 2x^2 + x - 3.
from scipy.optimize import root
import numpy as np

x0=0
def fun(x):
    return x**3-2*x*x+x-3
def find_root(fun,x0):
    ans=root(fun,x0)
    return ans.x
result=find_root(fun,x0)
print(result)