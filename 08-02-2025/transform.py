import numpy as np
from scipy.ndimage import geometric_transform

a = np.arange(12.).reshape((4, 3))
print(a)
def shift_func(output_coords):
    return (output_coords[0] - 0.5, output_coords[1] - 0.5)

ans=geometric_transform(a, shift_func)
print(ans)