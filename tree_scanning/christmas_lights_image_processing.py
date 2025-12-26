import cv2
import numpy as np
import my_utils

def load_image(light_num, folderPath):
    # Load the image
    return cv2.imread(f'{folderPath}/({light_num}).jpg')
    # return cv2.imread("C:/Users/jared/Pictures/Camera Roll/WIN_20251012_15_29_10_Pro.jpg")

def get_brightest_point(light_num, folderPath, display=False):

    image = load_image(light_num, folderPath)

    # Crop Image
    y_start = 0   # Starting y-coordinate (top)
    y_end = 1080   # Ending y-coordinate (bottom)
    x_start = 600 # Starting x-coordinate (left)
    x_end = 1920 - 600  # Ending x-coordinate (right)

    cropped_image = image[y_start:y_end, x_start:x_end]

    # Convert the image to grayscale for easier processing
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # (Optional) Apply a Gaussian blur to reduce noise, which can affect the brightest pixel detection
    blurred_image = cv2.GaussianBlur(gray_image, (41, 41), 0)

    # Find the minimum and maximum pixel values and their locations
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(blurred_image) # Use blurred_image for more robust detection

    # max_loc will contain the (x, y) coordinates of the brightest pixel
    brightest_pixel_coordinates = max_loc

    # You can also get the value of the brightest pixel
    brightest_pixel_value = max_val

    print(f"Brightest pixel value: {brightest_pixel_value}")
    print(f"Brightest pixel coordinates (x, y): {brightest_pixel_coordinates}")

    if display:
        # (Optional) Draw a circle around the brightest pixel for visualization
        cv2.circle(cropped_image, brightest_pixel_coordinates, 20, (0, 0, 255), 2) # Red circle with radius 20

        # Display the image with the brightest pixel marked
        cv2.imshow('Image with Brightest Pixel', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return brightest_pixel_coordinates

def get_upright_coord(coord):
    # y coordinate needs fliped (Image is 1920x1080)
    return [coord[0], 1080 - coord[1]]

def generateCoordinatesFromImages(numImages, folderPath):
    coords = []
    for i in range(1, numImages + 1):
        coords.append(get_brightest_point(i, folderPath))
    # write coordinates to text file seperated by commas
    # with open(f"{folderPath.rsplit('/', 1)[-1]}_Coords.txt", "w") as file:
    #     file.write(tempstr)
    return coords

# Format:
# [[(fx1,fy1), (rx1,ry1), (bx1,by1), (lx1,ly1)], [light2], [light3], ...]
# fx = Front x value, fy = Front y value, b = Back, r = Right, l = Left
def packageDirectionalCoordinateListsTogether():
    # Read in coordinates
    frontCoords = my_utils.read_in_coords("3D Tree Coords/Front_Facing_Coords.txt")
    rightCoords = my_utils.read_in_coords("3D Tree Coords/Right_Facing_Coords.txt")
    backCoords = my_utils.read_in_coords("3D Tree Coords/Back_Facing_Coords.txt")
    leftCoords = my_utils.read_in_coords("3D Tree Coords/Left_Facing_Coords.txt")

    # resulting string to write to file
    result = []

    for i in range(550):
        coordsForSingleLight = []
        coordsForSingleLight.append(frontCoords[i])
        coordsForSingleLight.append(rightCoords[i])
        coordsForSingleLight.append(backCoords[i])
        coordsForSingleLight.append(leftCoords[i])
        result.append(coordsForSingleLight)
    
    # Write to text file
    with open("All_Direction_Coords.txt", "w") as file:
        file.write(f"{result}")