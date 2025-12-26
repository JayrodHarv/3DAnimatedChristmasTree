import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from utils import my_utils

# --- Visualization ---

coords = np.array(my_utils.read_in_coords("tree_d_coords.txt"))

# Load coordinates (if you already have them saved)
# data = np.array([r[1:] for r in results])  # skip LightID

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot of all lights
ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], s=10, c='green', marker='o')

# Set axis labels
ax.set_xlabel('X (inches)')
ax.set_ylabel('Y (inches)')
ax.set_zlabel('Z (inches)')

# Keep aspect ratio roughly equal
max_range = np.ptp(coords, axis=0).max() / 2
mid_x = np.mean(coords[:, 0])
mid_y = np.mean(coords[:, 1])
mid_z = np.mean(coords[:, 2])
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.set_title("3D Reconstruction of Christmas Tree Lights")
ax.view_init(elev=20, azim=45)

plt.show()