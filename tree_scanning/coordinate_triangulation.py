import numpy as np
import sys

# =========================================
# CONFIGURATION
# =========================================

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

# CAMERA_DISTANCE = 1905.0   # millimeters (was 75 inches)
FOCAL_LENGTH = 1200.0    # pixels (approx, adjust if needed)

# Image center (important)
CX = IMAGE_WIDTH / 2
CY = IMAGE_HEIGHT / 2


# =========================================
# ROTATION MATRICES
# =========================================

def rotation_x(theta):
    """Rotation matrix about X axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])


def rotation_z(theta):
    """Rotation matrix about Z axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])


# We want Z to be the "up" (height) axis. The camera's local Y is the image up
# direction, so pre-rotate camera coords by +90deg around X to map camera Y -> world Z.
# Then rotate around world Z to get the four 90-degree views around the tree.
ROTATIONS = [
    rotation_z(0) @ rotation_x(np.pi / 2),
    rotation_z(np.pi / 2) @ rotation_x(np.pi / 2),
    rotation_z(np.pi) @ rotation_x(np.pi / 2),
    rotation_z(3 * np.pi / 2) @ rotation_x(np.pi / 2),
]


# =========================================
# PIXEL -> RAY
# =========================================

def pixel_to_ray(u, v):
    """
    Convert pixel coordinate to normalized camera ray
    Camera looks down +Z
    """
    x = (u - CX) / FOCAL_LENGTH
    y = -(v - CY) / FOCAL_LENGTH  # flip Y (image coords)
    z = 1.0

    ray = np.array([x, y, z])
    return ray / np.linalg.norm(ray)


# =========================================
# TRIANGULATION
# =========================================

def triangulate_point(pixel_sets, camera_distance_mm):
    """
    pixel_sets: [(u0,v0), (u90,v90), (u180,v180), (u270,v270)]
    """

    origins = []
    directions = []

    for (u, v), R in zip(pixel_sets, ROTATIONS):
        ray = pixel_to_ray(u, v)
        ray = R @ ray

        origin = R @ np.array([0, 0, -camera_distance_mm])

        origins.append(origin)
        directions.append(ray)

    # Solve least squares intersection of rays
    A = np.zeros((3, 3))
    b = np.zeros(3)

    for o, d in zip(origins, directions):
        d = d / np.linalg.norm(d)
        I = np.eye(3)
        A += I - np.outer(d, d)
        b += (I - np.outer(d, d)) @ o

    point = np.linalg.solve(A, b)
    return point.tolist()


# =========================================
# MAIN PIPELINE
# =========================================

def triangulate_all(coords_0, coords_90, coords_180, coords_270, camera_distance_mm, display=False):
    """
    Each coords_* is a list of (u,v) pairs

    Args:
        display: if True, show progress bar while triangulating; otherwise run quietly.
    """

    assert len(coords_0) == len(coords_90) == len(coords_180) == len(coords_270)

    points_3d = []
    num_leds = len(coords_0)

    for i in range(num_leds):
        pixels = [
            coords_0[i],
            coords_90[i],
            coords_180[i],
            coords_270[i]
        ]
        p = triangulate_point(pixels, camera_distance_mm)
        points_3d.append(p)

        # Progress Bar
        percent = int((i + 1) / num_leds * 100)
        bar = "#" * (percent // 2) + "-" * (50 - percent // 2)

        sys.stdout.write(f"\rTriangulating: [{bar}] {percent}%")
        sys.stdout.flush()

    print(" Done!")
    return points_3d