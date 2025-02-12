import numpy as np
from scipy.stats import describe, gmean, hmean, mode, kurtosis, skew, iqr, entropy, sem


data = np.array([2, 8, 3, 5, 7, 8, 10, 8, 6, 9])

# 1. Compute several descriptive statistics
desc_stats = describe(data)
print("Descriptive Statistics:", desc_stats)

# 2. Compute the geometric mean
geo_mean = gmean(data)
print("Geometric Mean:", geo_mean)

# 3. Compute the harmonic mean
harm_mean = hmean(data)
print("Harmonic Mean:", harm_mean)

# 4. Find the mode (most frequent value)
mode_value = mode(data, keepdims=False)
print("Mode:", mode_value.mode)

# 5. Compute kurtosis (measure of tailedness)
kurt = kurtosis(data)
print("Kurtosis:", kurt)

# 6. Compute skewness (measure of asymmetry)
skewness = skew(data)
print("Skewness:", skewness)

# 7. Compute interquartile range (IQR)
iqr_value = iqr(data)
print("Interquartile Range (IQR):", iqr_value)

# 8. Compute standard error of the mean (SEM)
sem_value = sem(data)
print("Standard Error of Mean (SEM):", sem_value)

# 9. Compute Shannon entropy
probabilities = np.array([0.1, 0.2, 0.3, 0.4])  # Example probabilities
entropy_value = entropy(probabilities)
print("Shannon Entropy:", entropy_value)
