from scipy.optimize import root,minimize,fsolve
from math import cos

def fun(x):
  return x+cos(x)

myroot=root(fun,0)
print("root",myroot)
mymin = minimize(fun, 0,method="CG")
mymin = minimize(fun, 0,method="BFGS")
# method - name of the method to use. Legal values:
#     'CG'
#     'BFGS'
#     'Newton-CG'
#     'L-BFGS-B'
#     'TNC'
#     'COBYLA'
#     'SLSQP'
print(mymin.x)
