import matplotlib.pyplot as plt

# Create two figures with different sizes
fig1, ax1 = plt.subplots(figsize=(4, 3))  # Small figure (4x3 inches)
ax1.plot([1, 2, 3], [4, 5, 6])
ax1.set_title("Small Figure")

fig2, ax2 = plt.subplots(figsize=(8, 6))  # Larger figure (8x6 inches)
ax2.plot([1, 2, 3], [4, 5, 6])
ax2.set_title("Large Figure")

plt.show()
