import sys
import argparse
from tree_scanning import christmas_lights_image_processing, coordinate_triangulation
from utils import my_utils

# First, use the autohotkey macro to take pictures of each light from 4 directions differing by 90 degrees.

def parse_args():
    parser = argparse.ArgumentParser(
        description="3D Christmas Tree Coordinate Triangulation from Images"
    )

    parser.add_argument(
        "num_lights",
        type=int,
        help="Number of lights on the tree"
    )

    parser.add_argument(
        "camera_distance_mm",
        type=float,
        help="Distance from camera to center of tree in millimeters"
    )

    parser.add_argument(
        "front_facing_path",
        type=str,
        help="Path to front facing pictures"
    )

    parser.add_argument(
        "right_facing_path",
        type=str,
        help="Path to right facing pictures"
    )

    parser.add_argument(
        "back_facing_path",
        type=str,
        help="Path to back facing pictures"
    )

    parser.add_argument(
        "left_facing_path",
        type=str,
        help="Path to left facing pictures"
    )

    parser.add_argument(
        "output_filename",
        type=str,
        help="Output filename for saved coordinates"
    )

    parser.add_argument(
        "--display",
        action="store_true",
        help="Display graphs throughout processing"
    )

    return parser.parse_args()

args = parse_args()

files = [args.front_facing_path, args.right_facing_path, args.back_facing_path, args.left_facing_path]

def validate_file_paths(paths):
    import os
    for path in paths:
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist.")
            sys.exit(1)

validate_file_paths(files)

frontFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(args.num_lights, args.front_facing_path, "front facing", display=args.display)
rightFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(args.num_lights, args.right_facing_path, "right facing", display=args.display)
backFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(args.num_lights, args.back_facing_path, "back facing", display=args.display)
leftFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(args.num_lights, args.left_facing_path, "left facing", display=args.display)

coords = coordinate_triangulation.triangulate_all(frontFacingCoords, rightFacingCoords, backFacingCoords, leftFacingCoords, args.camera_distance_mm, display=args.display)

# TODO run coords through error correcting code

coords = my_utils.normalize_tree_coords(coords)

if args.display:
        # Show 3D graph using matplotlib with equal axis scaling so tree doesn't look smushed
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        zs = [p[2] for p in coords]
        ax.scatter(xs, ys, zs)
        ax.set_title("Triangulated 3D Coordinates")
        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.set_zlabel("Z (mm)")
        # Make x, y, z axes have equal scale and be centered
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        z_min, z_max = min(zs), max(zs)
        x_mid = (x_max + x_min) / 2.0
        y_mid = (y_max + y_min) / 2.0
        z_mid = (z_max + z_min) / 2.0
        max_range = max(x_max - x_min, y_max - y_min, z_max - z_min)
        half = max_range / 2.0
        ax.set_xlim(x_mid - half, x_mid + half)
        ax.set_ylim(y_mid - half, y_mid + half)
        ax.set_zlim(z_mid - half, z_mid + half)
        plt.show()

my_utils.save_coordinates(coords, args.output_filename)

print(f"Saved {len(coords)} points to {args.output_filename}")