import matplotlib.pyplot as plt

# Creating a bar chart with different hatching patterns
bars = plt.bar(['X', 'Y', 'Z'], [2, 4, 6], hatch='\\|/', color='cyan', edgecolor='black')

plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Multiple Hatch Patterns Demo')

plt.show()