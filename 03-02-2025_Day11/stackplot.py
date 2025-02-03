import matplotlib.pyplot as plt

# List of Days
days = [1, 2, 3, 4, 5]

# No of Study Hours
Studying = [7, 8, -6, 11, 7]

# No of Playing Hours 
playing = [-8, 5, 7, -8, 13]

# Stackplot with labels and baseline
plt.stackplot(days, Studying, playing,colors=['r', 'c'], baseline='zero',labels=['Study', 'Play'])
# plt.stackplot(days, Studying, playing,
#               colors=['r', 'c'], baseline='sym',
#               labels=['Study', 'Play'])
# plt.stackplot(days, Studying, playing,
#               colors=['r', 'c'], baseline='wiggle',
#               labels=['Study', 'Play'])
# plt.stackplot(days, Studying, playing,
#               colors=['r', 'c'], baseline='weighted_wiggle',
#               labels=['Study', 'Play'])

# Labels
plt.xlabel('Days')
plt.ylabel('No of Hours')
plt.title('Representation of Study and Playing w.r.t. Days')

# Legend
plt.legend()

# Displaying Graph
plt.show()
