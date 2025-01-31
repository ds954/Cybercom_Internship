from scipy.cluster.hierarchy import DisjointSet

# Create a DisjointSet with some initial elements
disjoint_set = DisjointSet([1, 2, 3, 'a', 'b'])

disjoint_set.add(4)  # Add element 4
print("Added 4 to the disjoint set.")

# Merging some elements
disjoint_set.merge(1, 2)  # Merge subsets containing 1 and 2
print("Merged subsets containing 1 and 2.")

disjoint_set.merge(3, 'a')  # Merge subsets containing 3 and 'a'
print("Merged subsets containing 3 and 'a'.")

disjoint_set.merge('a', 'b')  # Merge subsets containing 'a' and 'b'
print("Merged subsets containing 'a' and 'b'.")

# Checking if elements are connected
print("Are 1 and 2 connected?", disjoint_set.connected(1, 2))  # Check connection between 1 and 2
print("Are 1 and 'b' connected?", disjoint_set.connected(1, 'b'))  # Check connection between 1 and 'b'

# Getting the subset of an element
print("Subset containing 2:", disjoint_set.subset(2))  # Get subset containing 2

# Getting the size of the subset of element 'a'
print("Size of the subset containing 'a':", disjoint_set.subset_size('a'))  # Get size of subset containing 'a'

# Getting all subsets
print("All subsets:", disjoint_set.subsets())  # Get all subsets

# Finding the root of element 2
print("Root element of 2:", disjoint_set[2])  # Find root of element 2
print(disjoint_set.__getitem__(2))