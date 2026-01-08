import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from utils import my_utils
import argparse

DEFAULT_COORDS_FILE = "bottom_normalized_tree_d_coords_mm.txt" # set coords file as this by default

def parse_args():
    parser = argparse.ArgumentParser(
        description="3D Christmas Tree Visualization Tool"
    )

    parser.add_argument(
        "--coords",
        nargs="?",
        default=DEFAULT_COORDS_FILE,
        help="Path to coordinate file"
    )

    parser.add_argument(
        "--output",
        nargs="?",
        help="output file name"
    )

    return parser.parse_args()

args = parse_args()

INPUT_FILE = args.coords
OUTPUT_FILE = args.output

# Load coordinates in from file
original_coords = my_utils.read_in_coords(INPUT_FILE)
working_coords = list(original_coords)
preview_coords = None
incorrect_coords = []

def find_incorrect_points(coords, max_distance = 5):
    incorrect = set() # set so can't contain two of same point

    for i in range(len(coords) - 1):
        p1 = np.array(coords[i])
        p2 = np.array(coords[i + 1])

        # Add points to incorrect points if they are too far apart
        if np.linalg.norm(p2 - p1) > max_distance:
            incorrect.add(i)
            incorrect.add(i + 1)
    
    return sorted(incorrect)

def plot_coords(coords, bad_indices, title):
    ax.clear()

    xs, ys, zs = zip(*coords)
    ax.scatter(xs, ys, zs, c="green", s=8)

    if bad_indices:
        bx = [coords[i][0] for i in bad_indices]
        by = [coords[i][1] for i in bad_indices]
        bz = [coords[i][2] for i in bad_indices]

        ax.scatter(bx, by, bz, c="red", s=8)

    set_equal_3d_axes(ax, coords)

    ax.set_title(title)
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    plt.draw()

def set_equal_3d_axes(ax, coords):
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    zs = [p[2] for p in coords]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    z_min, z_max = min(zs), max(zs)

    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    max_range = max(x_range, y_range, z_range) / 2

    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2
    z_mid = (z_max + z_min) / 2

    ax.set_xlim(x_mid - max_range, x_mid + max_range)
    ax.set_ylim(y_mid - max_range, y_mid + max_range)
    ax.set_zlim(z_mid - max_range, z_mid + max_range)

def auto_correct(coords, bad_indices):
    fixed = list(coords)

    for i in bad_indices:
        if 0 < i < len(coords) - 1:
            p_prev = np.array(coords[i - 1])
            p_next = np.array(coords[i + 1])
            fixed[i] = tuple((p_prev + p_next) / 2)

    return fixed

# UI STUFF
def on_detect(event):
    global incorrect_coords
    incorrect_coords = find_incorrect_points(working_coords)
    plot_coords(working_coords, incorrect_coords, f"Detected {len(incorrect_coords)} bad points")

def on_preview(event):
    global preview_coords
    if not incorrect_coords: 
        return
    preview_coords = auto_correct(working_coords, incorrect_coords)
    plot_coords(preview_coords, incorrect_coords, "Preview of auto-corrected points")

def on_accept(event):
    global working_coords
    working_coords = preview_coords
    incorrect_coords.clear()
    plot_coords(working_coords, [], "Corrections accepted")

def on_reset(event):
    global working_coords, incorrect_coords
    working_coords[:] = original_coords
    incorrect_coords.clear()
    plot_coords(
        working_coords,
        [],
        "Reset to original"
    )

def on_save(event):
    with open(OUTPUT_FILE, "w") as f:
        for x, y, z in working_coords:
            f.write(f"[{x}, {y}, {z}]\n")
    print(f"Saved corrected file to: {OUTPUT_FILE}")

btn_detect_ax = plt.axes([0.1, 0.02, 0.15, 0.05])
btn_preview_ax = plt.axes([0.27, 0.02, 0.15, 0.05])
btn_accept_ax = plt.axes([0.44, 0.02, 0.15, 0.05])
btn_reset_ax  = plt.axes([0.61, 0.02, 0.15, 0.05])
btn_save_ax   = plt.axes([0.78, 0.02, 0.15, 0.05])

btn_detect = Button(btn_detect_ax, "Detect")
btn_preview = Button(btn_preview_ax, "Preview Fix")
btn_accept = Button(btn_accept_ax, "Accept Fix")
btn_reset = Button(btn_reset_ax, "Reset")
btn_save = Button(btn_save_ax, "Save Changes")

btn_detect.on_clicked(on_detect)
btn_preview.on_clicked(on_preview)
btn_accept.on_clicked(on_accept)
btn_reset.on_clicked(on_reset)
btn_save.on_clicked(on_save)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

plot_coords(working_coords, [], "Original Coordinates")

# Keep aspect ratio roughly equal
# max_range = np.ptp(working_coords, axis=0).max() / 2
# mid_x = np.mean(working_coords[:, 0])
# mid_y = np.mean(working_coords[:, 1])
# mid_z = np.mean(working_coords[:, 2])
# ax.set_xlim(mid_x - max_range, mid_x + max_range)
# ax.set_ylim(mid_y - max_range, mid_y + max_range)
# ax.set_zlim(mid_z - max_range, mid_z + max_range)

# ax.set_title("3D Reconstruction of Christmas Tree Lights")
# ax.view_init(elev=20, azim=45)

plt.show()