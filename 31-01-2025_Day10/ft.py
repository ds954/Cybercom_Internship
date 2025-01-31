import numpy as np
from scipy.fft import fft, ifft, fft2, ifft2, fftn, ifftn
from scipy.fft import rfft, irfft, rfft2, irfft2, rfftn, irfftn
from scipy.fft import hfft, ihfft, hfft2, ihfft2, hfftn, ihfftn

# 1D FFT and IFFT
arr = np.array([1, 2, 3, 4, 5, 6, 7])
fft_arr = fft(arr)  # Fast Fourier Transform
print("FFT:", fft_arr)
inversed_arr = ifft(fft_arr)  # Inverse Fast Fourier Transform
print("IFFT:", inversed_arr)

# 2D FFT and IFFT
arr2 = np.array([[1, 2, 3],
                 [4, 5, 6]])
fft2_arr = fft2(arr2)  # 2-Dimensional Fast Fourier Transform
print("FFT2:", fft2_arr)
inversed_arr2 = ifft2(fft2_arr)  # Inverse 2-Dimensional Fast Fourier Transform
print("IFFT2:", inversed_arr2)

# N-D FFT and IFFT
arr3 = np.random.rand(3, 3, 3)
fftn_arr = fftn(arr3)  # N-Dimensional Fast Fourier Transform
print("FFTN:", fftn_arr)
inversed_arr3 = ifftn(fftn_arr)  # Inverse N-Dimensional Fast Fourier Transform
print("IFFTN:", inversed_arr3)

# Real-input FFT and IFFT
rfft_arr = rfft(arr)  # Real Fast Fourier Transform (optimized for real-valued input)
print("RFFT:", rfft_arr)
irfft_arr = irfft(rfft_arr)  # Inverse Real Fast Fourier Transform
print("IRFFT:", irfft_arr)

rfft2_arr = rfft2(arr2)  # 2-Dimensional Real Fast Fourier Transform
print("RFFT2:", rfft2_arr)
irfft2_arr = irfft2(rfft2_arr)  # Inverse 2-Dimensional Real Fast Fourier Transform
print("IRFFT2:", irfft2_arr)

rfftn_arr = rfftn(arr3)  # N-Dimensional Real Fast Fourier Transform
print("RFFTN:", rfftn_arr)
irfftn_arr = irfftn(rfftn_arr)  # Inverse N-Dimensional Real Fast Fourier Transform
print("IRFFTN:", irfftn_arr)

