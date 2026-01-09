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

coords = coordinate_triangulation.triangulate_all(frontFacingCoords, rightFacingCoords, backFacingCoords, leftFacingCoords, display=args.display)

# TODO run coords through error correcting code

coords = my_utils.normalize_tree_coords(coords)

my_utils.save_coordinates(coords, args.output_filename)

print(f"Saved {len(coords)} points to {args.output_filename}")