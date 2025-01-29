import numpy as np

arr=np.array([np.pi/2, np.pi/3, np.pi/4, np.pi/5])
print("sin value: ",np.sin(arr))
print("\nhyperbolic sin value: ")
print(np.sinh(arr))

radian_to_degree=np.rad2deg(arr)
print("\n radian to degree val: \n",radian_to_degree)

degree_val=np.array([15,45,0,180])
print("\ndegree to radian: \n",np.deg2rad(degree_val))


base=8
perp=6
print(np.hypot(base, perp))

