import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import my_utils

# --- Load tree points ---
# Replace with your path if needed
points = np.asarray(my_utils.read_in_coords("tree_d_coords.txt"))

# Center points around origin for nicer visuals (optional)
center = np.mean(points, axis=0)
points_centered = points - center

# --- Animation parameters ---
num_planes = 4               # number of moving planes
speed_range = (0.5, 1.2)     # speed of plane movement (units/frame)
thickness = 5.0              # how thick each lighting band is (in same units as points)
extent = np.max(np.ptp(points_centered, axis=0)) / 2.0

# --- Generate random plane directions and speeds ---
rng = np.random.default_rng(42)
normals = rng.normal(size=(num_planes, 3))
normals /= np.linalg.norm(normals, axis=1)[:, None]   # shape (num_planes, 3)
speeds = rng.uniform(*speed_range, size=num_planes)   # shape (num_planes,)
offsets = rng.uniform(-extent, extent, size=num_planes)  # initial offsets

# Colors
gold = np.array([1.0, 0.84, 0.0])   # RGB for lit lights
dark = np.array([0.2, 0.2, 0.2])    # RGB for off lights

# --- Visualization setup ---
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-extent, extent)
ax.set_ylim(-extent, extent)
ax.set_zlim(-extent, extent)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Multiple Planes Sweeping Through the Tree")

# initial gray color for all points (RGBA)
N = points_centered.shape[0]
init_colors = np.tile(dark, (N, 1))
init_alphas = np.ones((N, 1))
init_rgba = np.hstack((init_colors, init_alphas))

sc = ax.scatter(points_centered[:,0], points_centered[:,1], points_centered[:,2],
                c=init_rgba, s=12)

# --- Animation update function ---
def update(frame):
    global offsets
    # Advance offsets linearly
    offsets = offsets + speeds
    # Wrap offsets so planes re-enter from other side
    offsets = np.where(offsets > extent, -extent, offsets)

    # Compute signed distances of every point to every plane
    # distances shape: (N, num_planes)
    distances = points_centered @ normals.T + offsets  # broadcasting: (N,3) @ (3,num_planes) -> (N,num_planes)
    abs_dist = np.abs(distances)

    # For each point, get minimum absolute distance to any plane
    min_dist = np.min(abs_dist, axis=1)  # shape (N,)

    # Brightness: 1 at plane center, linear falloff to 0 at thickness/2
    half_thick = thickness / 2.0
    brightness = np.clip(1.0 - (min_dist / half_thick), 0.0, 1.0)  # shape (N,)

    # Build colors: lerp between dark and gold using brightness
    # colors_rgb shape: (N, 3)
    colors_rgb = dark[None, :] * (1.0 - brightness)[:, None] + gold[None, :] * brightness[:, None]

    # Optionally map brightness to alpha too
    alphas = 0.2 + 0.8 * brightness  # alpha in [0.2, 1.0]
    colors_rgba = np.hstack((colors_rgb, alphas[:, None]))

    # Update scatter points and colors
    sc._offsets3d = (points_centered[:,0], points_centered[:,1], points_centered[:,2])
    # Use set_facecolors (works well) — ensure shape (N,4)
    sc.set_facecolors(colors_rgba)
    sc.set_edgecolors(colors_rgba)

    return sc,

# --- Run animation ---
ani = FuncAnimation(fig, update, frames=1000, interval=60, blit=False)
plt.show()
