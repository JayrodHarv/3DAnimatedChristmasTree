import ast
import random
import colorsys
import numpy as np

good_colors = [
	(255,0,0),     # Red
	(0,255,0),     # Green
	(0,0,255),     # Blue
	(255,255,0),   # Yellow
	(127,0,255),    # Purple
	(255,127,0),    # Orange
	(255,255,255), # White
	(255,0,255),   # Pink
	(0,127,255),    # Navy Blue
	(255,0,127),    # Magenta
	(0,255,255)    # Lime Green
]

def get_random_good_color():
    return good_colors[random.randint(0,len(good_colors)-1)]

def generate_pleasant_colors(n=12, saturation=1, value=1):
    colors = []
    for i in range(n):
        h = i / n
        r, g, b = colorsys.hsv_to_rgb(h, saturation, value)
        colors.append((
            int(r * 255),
            int(g * 255),
            int(b * 255)
        ))
    return colors

def read_in_coords(filename):
    coords = []
    try:
        with open(filename, "r") as file:
            for line in file:
                coords.append(ast.literal_eval(line.strip()))
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error has occured.")

    return coords

def save_coordinates(points, filename):
    with open(filename, "w") as f:
        for p in points:
            f.write(f"{[p[0], p[1], p[2]]}\n")

def normalize_tree_coords(coords):
    """
    Normalize tree coordinates so that:
    - X=0, Y=0 is the trunk center
    - Z=0 is the bottom of the tree
    """

    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    zs = [p[2] for p in coords]

    # Bottom of tree
    z_min = min(zs)

    # Horizontal trunk center (centroid)
    x_center = sum(xs) / len(xs)
    y_center = sum(ys) / len(ys)

    normalized = []
    for x, y, z in coords:
        normalized.append((
            x - x_center,
            y - y_center,
            z - z_min
        ))

    return normalized

def inches_to_mm_rounded(coords):
    """
    Convert a list of 3D coordinates from inches to millimeters
    and round to the nearest millimeter.

    coords: iterable of (x, y, z) in inches
    returns: list of (x, y, z) in millimeters (ints)
    """
    INCH_TO_MM = 25.4

    return [
        (
            round(x * INCH_TO_MM),
            round(y * INCH_TO_MM),
            round(z * INCH_TO_MM),
        )
        for x, y, z in coords
    ]

def flip_rightway(filename):
    coords = read_in_coords(filename)
    for coord in coords:
        coord[1], coord[2] = coord[2], coord[1]
    
    # write to file
    result = ""
    for coord in coords:
        result += f"{coord}\n"
    with open("tree_d_coords.txt", "w") as file:
        file.write(f"{result}")

def rotate_coordinates_around_average(coordinates, angle_degrees):
    """
    Rotates a list of 2D coordinates around their average point.

    Args:
        coordinates (list or np.ndarray): A list of (x, y) tuples or a NumPy array
                                         of shape (N, 2) representing the coordinates.
        angle_degrees (float): The rotation angle in degrees (positive for counter-clockwise).

    Returns:
        np.ndarray: A NumPy array of the rotated coordinates.
    """
    coordinates = np.array(coordinates)

    # 1. Calculate the average point (centroid)
    average_point = np.mean(coordinates, axis=0)

    # 2. Translate coordinates to the origin
    translated_coordinates = coordinates - average_point

    # Convert angle to radians
    angle_radians = np.deg2rad(angle_degrees)

    # Create the 2D rotation matrix
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])

    # 3. Rotate the translated coordinates
    rotated_translated_coordinates = np.dot(translated_coordinates, rotation_matrix.T)

    # 4. Translate back to the original position
    rotated_coordinates = rotated_translated_coordinates + average_point

    return rotated_coordinates

def randomly_rotate_tree(points):
    """
    Rotates a set of 3D tree coordinates so that the tree's 'up' axis
    points in a random direction in 3D space.

    Args:
        points (np.ndarray): shape (N, 3) array of [x, y, z] coordinates.

    Returns:
        np.ndarray: shape (N, 3) array of rotated coordinates.
    """
    points = np.asarray(points)

    # Compute the centroid to rotate around the tree's center
    center = np.mean(points, axis=0)
    centered_points = points - center

    # Define the tree's current "up" direction (Z-axis)
    up = np.array([0, 0, 1], dtype=float)

    # Generate a random unit vector as the new "up" direction
    rand_vec = np.random.normal(size=3)
    rand_vec /= np.linalg.norm(rand_vec)

    # If the random vector happens to be very close to the current up vector, skip rotation
    if np.allclose(rand_vec, up, atol=1e-6):
        return points.copy()

    # Compute rotation axis (cross product) and angle (dot product)
    axis = np.cross(up, rand_vec)
    axis /= np.linalg.norm(axis)
    angle = np.arccos(np.clip(np.dot(up, rand_vec), -1.0, 1.0))

    # Rodrigues' rotation formula to create rotation matrix
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)

    # Rotate and re-add center
    rotated_points = centered_points @ R.T + center

    return rotated_points


def _set_axes_equal(ax):
    """Set 3D plot axes to equal scale (works for matplotlib 3D axes).

    Based on code in TreeVisualizer._set_axes_equal so the plot isn't
    visually distorted when axis ranges differ.
    """
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


def plot_tree_3d(coords, colors=None, point_size=20, ax=None, elev=None, azim=None, show=True, title=None):
    """Create (and optionally display) a 3D scatter plot of tree coordinates.

    Args:
        coords: Iterable of (x, y, z) tuples or an (N,3) numpy array.
        colors: Optional color specification. Can be:
            - None: default to black
            - single RGB tuple/list (r,g,b) in 0-255 or 0-1
            - iterable of per-point colors as (r,g,b) 0-255 or 0-1
        point_size: Marker size for scatter points.
        ax: Optional matplotlib 3D axes to draw into. If omitted, a new
            Figure and 3D Axes will be created.
        elev, azim: Optional elevation/azimuth for the initial view.
        show: If True and a new figure was created, call plt.show(). If an
            `ax` was provided, show is ignored.
        title: Optional title for the plot.

    Returns:
        (fig, ax, scatter) where fig may be None if `ax` was provided and the
        caller manages the Figure externally.
    """
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        raise ImportError("matplotlib is required for plotting: " + str(e))

    arr = np.asarray(coords)
    if arr.size == 0:
        raise ValueError("No coordinates provided to plot_tree_3d")
    if arr.ndim != 2 or arr.shape[1] != 3:
        raise ValueError("coords must be an (N,3) array or iterable of (x,y,z)")

    created_fig = False
    if ax is None:
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        created_fig = True
    else:
        fig = ax.figure

    xs, ys, zs = arr[:, 0], arr[:, 1], arr[:, 2]

    # Prepare colors: normalize to 0-1 tuples
    def _normalize_color(c):
        c = tuple(c)
        if all(isinstance(v, int) for v in c):
            return tuple(v / 255.0 for v in c)
        return tuple(float(v) for v in c)

    if colors is None:
        cols = [(0.0, 0.0, 0.0)] * len(xs)
    else:
        # Single color
        if not hasattr(colors, '__len__') or isinstance(colors[0], (int, float)):
            cols = [_normalize_color(colors)] * len(xs)
        else:
            # Per-point sequence
            cols = [_normalize_color(c) for c in colors]

    sc = ax.scatter(xs, ys, zs, c=cols, s=point_size)

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    if title:
        ax.set_title(title)

    # Set equal axis scaling for nicer visuals
    try:
        _set_axes_equal(ax)
    except Exception:
        pass

    if elev is not None or azim is not None:
        elev_val = elev if elev is not None else getattr(ax, 'elev', None)
        azim_val = azim if azim is not None else getattr(ax, 'azim', None)
        if elev_val is not None and azim_val is not None:
            ax.view_init(elev=elev_val, azim=azim_val)

    if created_fig and show:
        plt.show()

    return fig, ax, sc


def plot_2d_coords_flipped(coords, ax=None, point_size=20, color='b', title=None, show=True):
    """Simple helper that flips Y and labels ticks with original units.

    - Flips Y by multiplying by -1 (useful for image coordinates where Y
      increases downward).
    - Replaces Y tick labels with negated values so labels show original units.
    """
    import matplotlib.pyplot as plt

    arr = np.asarray(coords)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError("coords must be an (N,2) array or iterable of (x,y)")

    x = arr[:, 0]
    y = -arr[:, 1]

    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
        created_fig = True
    else:
        fig = ax.figure

    sc = ax.scatter(x, y, c=color, s=point_size)

    ax.set_xlabel('X')
    ax.set_ylabel('Y (original units)')
    if title:
        ax.set_title(title)

    # Use a FuncFormatter to display original (pre-flip) Y units by negating
    # the tick values. This avoids setting tick labels directly and the
    # associated Matplotlib warning about FixedFormatter/FixedLocator.
    from matplotlib.ticker import FuncFormatter
    def _fmt(y, pos):
        try:
            if float(y).is_integer():
                return str(int(-y))
        except Exception:
            pass
        return f"{(-y):.2f}"
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt))

    if created_fig and show:
        plt.show()

    return fig, ax, sc