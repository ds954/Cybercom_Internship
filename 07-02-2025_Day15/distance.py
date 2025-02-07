from scipy.spatial import minkowski_distance


# p=1, it becomes Manhattan Distance.
# p=2, it becomes Euclidean Distance.

ans=minkowski_distance([[7,8], [5, 2]], [[3, 1], [0, 1]],p=5)
print(ans)