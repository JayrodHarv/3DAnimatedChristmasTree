import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math
from utils import my_utils

def create_3D_graph(correct):
    # --- Visualization ---

    # Load coordinates (if you already have them saved)
    # data = np.array([r[1:] for r in results])  # skip LightID

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot of all lights
    ax.scatter(correct[:, 0], correct[:, 1], correct[:, 2], s=10, c='green', marker='o')
    # ax.scatter(incorrect[:, 0], incorrect[:, 1], incorrect[:, 2], s=10, c='red', marker='o')

    # Set axis labels
    ax.set_xlabel('X (inches)')
    ax.set_ylabel('Y (inches)')
    ax.set_zlabel('Z (inches)')

    # Keep aspect ratio roughly equal
    max_range = np.ptp(correct, axis=0).max() / 2
    mid_x = np.mean(correct[:, 0])
    mid_y = np.mean(correct[:, 1])
    mid_z = np.mean(correct[:, 2])
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.set_title("3D Reconstruction of Christmas Tree Lights")
    ax.view_init(elev=20, azim=45)

    plt.show()

def distance_apart(coord1, coord2):
    return math.sqrt(abs(coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 + (coord1[2] - coord2[2])**2)

def find_incorrect_coords(coords):
    MAX_DISTANCE_APART = 5 + 2 # in inches
    incorrect = []
    corrected = coords.copy()
    for i in range(1, len(coords) - 1):
        d_prev = np.linalg.norm(coords[i] - coords[i-1])
        d_next = np.linalg.norm(coords[i] - coords[i+1])
        if d_prev > MAX_DISTANCE_APART or d_next > MAX_DISTANCE_APART:
            incorrect.append(coords[i])
            corrected[i] = (coords[i - 1] + coords[i + 1]) / 2  # simple average replacement
    return corrected

def setdiff2d(A, B):
    A_view = A.view([('', A.dtype)] * A.shape[1])
    B_view = B.view([('', B.dtype)] * B.shape[1])
    return np.setdiff1d(A_view, B_view).view(A.dtype).reshape(-1, A.shape[1])

def main():
    coords = np.asarray(my_utils.read_in_coords("tree_d_coords.txt"))
    # incorrect = np.asarray(find_incorrect_coords(coords))
    # correct = setdiff2d(coords, incorrect)
    # print(correct)

    coords = find_incorrect_coords(coords)
    create_3D_graph(coords)

    my_utils.save_coordinates(coords.tolist(), "corrected_3D_coords")

main()