import sys
from tree_scanning import christmas_lights_image_processing, coordinate_triangulation
from utils import my_utils

# First, use the autohotkey macro to take pictures of each light from 4 directions differing by 90 degrees.

args = sys.argv[1:] # first argument is the name of script

if (len(args) < 5):
    print("Usage: python ScanTree.py <number of lights> <path to front facing pictures> <path to right facing pictures> <path to back facing pictures> <path to left facing pictures> <output file name>")
    sys.exit(1)

try:
    NUM_LIGHTS = int(args[0])
except:
    print("Invalid number of lights. Please try again...")

FRONT_FACING_PATH = args[1]
RIGHT_FACING_PATH = args[2]
BACK_FACING_PATH = args[3]
LEFT_FACING_PATH = args[4]
OUTPUT_FILENAME = args[5]

frontFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, FRONT_FACING_PATH, "front facing")
rightFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, RIGHT_FACING_PATH, "right facing")
backFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, BACK_FACING_PATH, "back facing")
leftFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, LEFT_FACING_PATH, "left facing")

coords = coordinate_triangulation.triangulate_all(frontFacingCoords, rightFacingCoords, backFacingCoords, leftFacingCoords)

# TODO run coords through error correcting code

coords = coordinate_triangulation.normalize_tree_coords(coords)

my_utils.save_coordinates(coords, OUTPUT_FILENAME)

print(f"Saved {len(coords)} points to {OUTPUT_FILENAME}")