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

def generate_pleasant_colors(n=12, saturation=0.75, value=1):
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
    - Z=0 is the vertical midpoint of the tree
    """

    # SWAP Y AND Z
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    zs = [p[2] for p in coords]

    center_x = sum(xs) / len(xs)
    center_y = sum(ys) / len(ys)

    min_z = min(zs)
    max_z = max(zs)
    center_z = (min_z + max_z) / 2

    normalized = []
    for x, y, z in coords:
        normalized.append((
            x - center_x,
            y - center_y,
            z - center_z
        ))

    return normalized

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