import numpy as np

# =========================================
# CONFIGURATION
# =========================================

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 920

CAMERA_DISTANCE = 75.0   # inches (or cm, units stay consistent)
FOCAL_LENGTH = 1200.0    # pixels (approx, adjust if needed)

OUTPUT_FILE = "tree_coords_3d.txt"

# Image center (important)
CX = IMAGE_WIDTH / 2
CY = IMAGE_HEIGHT / 2


# =========================================
# ROTATION MATRICES
# =========================================

def rotation_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])


ROTATIONS = [
    rotation_y(0),
    rotation_y(np.pi / 2),
    rotation_y(np.pi),
    rotation_y(3 * np.pi / 2),
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

def triangulate_point(pixel_sets):
    """
    pixel_sets: [(u0,v0), (u90,v90), (u180,v180), (u270,v270)]
    """

    origins = []
    directions = []

    for (u, v), R in zip(pixel_sets, ROTATIONS):
        ray = pixel_to_ray(u, v)
        ray = R @ ray

        origin = R @ np.array([0, 0, -CAMERA_DISTANCE])

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
    return point


# =========================================
# MAIN PIPELINE
# =========================================

def triangulate_all(coords_0, coords_90, coords_180, coords_270):
    """
    Each coords_* is a list of (u,v) pairs
    """

    assert len(coords_0) == len(coords_90) == len(coords_180) == len(coords_270)

    points_3d = []

    for i in range(len(coords_0)):
        pixels = [
            coords_0[i],
            coords_90[i],
            coords_180[i],
            coords_270[i]
        ]
        p = triangulate_point(pixels)
        points_3d.append(p)

    return np.array(points_3d)


# =========================================
# SAVE OUTPUT
# =========================================

def save_txt(points, filename):
    with open(filename, "w") as f:
        for p in points:
            f.write(f"{p}\n")


# =========================================
# EXAMPLE USAGE
# =========================================

if __name__ == "__main__":

    # Replace these with your real data
    coords_0   = [(500, 400)] * 550
    coords_90  = [(520, 410)] * 550
    coords_180 = [(510, 420)] * 550
    coords_270 = [(490, 415)] * 550

    points_3d = triangulate_all(coords_0, coords_90, coords_180, coords_270)

    save_txt(points_3d, OUTPUT_FILE)

    print(f"Saved {len(points_3d)} points to {OUTPUT_FILE}")
