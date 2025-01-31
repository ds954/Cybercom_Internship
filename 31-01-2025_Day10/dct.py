import numpy as np
from scipy.fft import dct, idct, dctn, idctn, dst, idst, dstn, idstn, fht, ifht

# 1D DCT and IDCT
x = np.array([1, 2, 3, 4, 5])
dct_x = dct(x, type=2)  # Type 2 is common
print("DCT:", dct_x)
idct_x = idct(dct_x, type=2)
print("IDCT:", idct_x)

# 2D DCT and IDCT (e.g., for a small image-like array)
image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
dct2_image = dctn(image, type=2, axes=(0, 1))  # Apply DCT along both axes
print("2D DCT:\n", dct2_image)
idct2_image = idctn(dct2_image, type=2, axes=(0, 1))
print("2D IDCT:\n", idct2_image)

# 1D DST and IDST
y = np.array([1, 2, 3, 4, 5])
dst_y = dst(y, type=2)
print("DST:", dst_y)
idst_y = idst(dst_y, type=2)
print("IDST:", idst_y)

# N-D DST (example with a 3D array)
data_3d = np.random.rand(3, 4, 5)
dst3d = dstn(data_3d, type=2, axes=(0, 1, 2)) # Apply DST along all 3 dimensions
print("3D DST:\n", dst3d)
idst3d = idstn(dst3d, type=2, axes=(0, 1, 2))
print("3D IDST:\n", idst3d)


# Fast Hankel Transform (FHT) - Example
# Note: FHT requires specific input parameters (a, dln, mu)

# Example values 
a = np.array([1.0, 2.0, 3.0, 4.0])  
dln = 0.1
mu = 1.0  

fht_result = fht(a, dln, mu)
print("FHT:", fht_result)

ifht_result = ifht(fht_result, dln, mu) # Inverse transform
print("IFHT:", ifht_result)


