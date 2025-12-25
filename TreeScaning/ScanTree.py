import sys
import christmas_lights_image_processing

# First, use the autohotkey macro to take pictures of each light from 4 directions differing by 90 degrees.

args = sys.argv[1:] # first argument is the name of script

if (len(args) < 5):
    print("Usage: python ScanTree.py <number of lights> <path to front facing pictures> <path to right facing pictures> <path to back facing pictures> <path to left facing pictures>")
    sys.exit(1)

NUM_LIGHTS = args[0]
FRONT_FACING_PATH = args[1]
RIGHT_FACING_PATH = args[2]
BACK_FACING_PATH = args[3]
LEFT_FACING_PATH = args[4]

try:
    frontFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, FRONT_FACING_PATH)
    rightFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, RIGHT_FACING_PATH)
    backFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, BACK_FACING_PATH)
    leftFacingCoords = christmas_lights_image_processing.generateCoordinatesFromImages(NUM_LIGHTS, LEFT_FACING_PATH)
except:
    print("Something went wrong while processing images")