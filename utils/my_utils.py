import ast
import random
import numpy as np

good_colors = [
	(255,0,0),     # Red
	(0,255,0),     # Blue
	(0,0,255),     # Green
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