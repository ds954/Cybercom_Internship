import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

# Defining control points 
verts = [(0, 0), (-0.5, 1), (2, -1), (3, 0)]


path = mpath.Path(verts, [mpath.Path.MOVETO, mpath.Path.CURVE4, mpath.Path.CURVE4, mpath.Path.CURVE4])


patch = mpatches.PathPatch(path, lw=2)


fig, ax = plt.subplots()
ax.add_patch(patch)

ax.scatter(*zip(*verts), c='red', marker='o')  
ax.set_xlim(-1, 4)
ax.set_ylim(-2, 2)
plt.title('Simple Bezier Curve')
plt.show()