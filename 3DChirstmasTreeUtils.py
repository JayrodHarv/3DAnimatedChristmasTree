import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import ast
import random
import cv2

# Usefull Constants
NUM_LIGHTS = 550

good_colors = [
	(127,0,0),     # Red
	(0,127,0),     # Blue
	(0,0,127),     # Green
	(127,127,0),   # Yellow
	(63,0,127),    # Purple
	(127,63,0),    # Orange
	(127,127,127), # White
	(127,0,127),   # Pink
	(0,63,127),    # Navy Blue
	(127,0,63),    # Magenta
	(0,127,127)    # Lime Green
]

def get_random_good_color():
    return good_colors[random.randint(0,len(good_colors)-1)]


def read_in_coords(coordsFileName):
    """Reads in 2D or 3D coordinates from a text file
    Text file must be formatted as such:
    In 2D:
        [453, 823] # First coord
        [428, 622] # Second coord
        [299, 469] # ...
    In 3D:
        [-4.987695261541013, 9.424246020924455, -33.12578507720924] # First coord
        [0.4073332521737267, 1.75610355216681, -34.7284111735123] # Second coord
        [-7.501739182366976, 11.284308557011352, -35.82647154959058] # ...
    These coords are in inches and relative to the center of the tree which is the origin(0,0,0)
    """
    coords = []
    try:
        with open(coordsFileName, "r") as file:
            for line in file:
                coords.append(ast.literal_eval(line.strip()))
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error has occured.")

    return coords

# --------------------------------------- #
#             IMAGE PROCESSING            #
# --------------------------------------- #

# All images are jpg's and stored in the following file structure:
# - *root folder*
#   - Front_Facing
#       - (1).jpg
#       - (2).jpg
#       - ...
#   - Right_Facing
#       - images...
#   - Back_Facing
#       - images
#   - Left_Facing
#       - images
# Note: I used a AutoHotKey macro to take all the pictures (~2000 total)
#       It switches between the camera app and my remote terminal into the Raspberry pi 
#       which runs a script I wrote to increment which light is on when enter is pressed.
# Another Note (Arguably more important than the last): In order to extrapolate 3D coordinates from the tree,
#       you need to take a picture of each light and do so from 4 different directions by rotating the tree 90 degrees 4 times.
#       I seperated those images into different folders to keep them straight

def load_image(light_num, folderPath):
    # Load the image
    return cv2.imread(f'{folderPath}/({light_num}).jpg')

def get_brightest_point(light_num, folderPath, display=False):
    # Crops out unneeded space on left and right of tree
    X_CROP = 600

    image = load_image(light_num, folderPath)

    # Crop Image
    y_start = 0   # Starting y-coordinate (top)
    y_end = 1080   # Ending y-coordinate (bottom)
    x_start = X_CROP # Starting x-coordinate (left)
    x_end = 1920 - X_CROP  # Ending x-coordinate (right)

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

def generate_coords_from_images(folderPath, writeToFile=False):
    tempstr = ""
    coords = []
    for i in range(1, NUM_LIGHTS + 1):
        coord = get_brightest_point(i, folderPath)
        coords.append(coord)
        # coords = get_upright_coord(coords)
        if writeToFile:
            tempstr += f"{coord}\n"
    if writeToFile:
        # write coordinates to text file seperated by commas
        with open(f"{folderPath.rsplit('/', 1)[-1]}_Coords.txt", "w") as file:
            file.write(tempstr)
    return coords

def generate_3D_coords_from_images(folderPath):
    # Read in coordinates
    frontCoords = read_in_coords("3D Tree Coords/Front_Facing_Coords.txt")
    rightCoords = read_in_coords("3D Tree Coords/Right_Facing_Coords.txt")
    backCoords = read_in_coords("3D Tree Coords/Back_Facing_Coords.txt")
    leftCoords = read_in_coords("3D Tree Coords/Left_Facing_Coords.txt")

    # resulting string to write to file
    result = []

    for i in range(NUM_LIGHTS):
        coordsForSingleLight = []
        coordsForSingleLight.append(frontCoords[i])
        coordsForSingleLight.append(rightCoords[i])
        coordsForSingleLight.append(backCoords[i])
        coordsForSingleLight.append(leftCoords[i])
        result.append(coordsForSingleLight)
    
    # Write to text file
    with open("All_Direction_Coords.txt", "w") as file:
        file.write(f"{result}")


def extract_xyz_from_csv(path):
    """
    Reads a CSV with columns:
    LightID,X,Y,Z,reproj_mean_px,reproj_0_px,reproj_90_px,reproj_180_px,reproj_270_px
    and returns Nx3 array of [x,y,z].
    """
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return data[:, 1:4].tolist()

# xyz = extract_xyz_from_csv("tree_3d_coordinates.csv")
# # print(xyz)
# result = ""
# for coord in xyz:
#     result += f"{coord}\n"
# with open("tree_d_coords.txt", "w") as file:
#     file.write(f"{result}")

# --------------------------------------- #
#             VISUALIZATIONS              #
# --------------------------------------- #

def show3DCoords(coordsFileName):
    """Takes in a file name and reads in the coords from the file and displays them by plotting the coords on a 3D graph
    """
    coords = np.array(read_in_coords(coordsFileName))

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot of all lights
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], s=10, c='green', marker='o')

    # Set axis labels
    ax.set_xlabel('X (inches)')
    ax.set_ylabel('Y (inches)')
    ax.set_zlabel('Z (inches)')

    # Keep aspect ratio roughly equal
    max_range = np.ptp(coords, axis=0).max() / 2
    mid_x = np.mean(coords[:, 0])
    mid_y = np.mean(coords[:, 1])
    mid_z = np.mean(coords[:, 2])
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.set_title("3D Reconstruction of Christmas Tree Lights")
    ax.view_init(elev=20, azim=45)

    plt.show()

# Exampe Usage:
# show3DCoords("tree_d_coords.txt")

def print_menu():
    print("3D Christmas Tree Main Menu:")
    print("(1) - Scan Tree")
    print("(2) - Graph 3D Coordinates of Tree")
    print("(3) - Generate 3D Coordinates From Images")

def main():
    # command line interface to run certain functions
    print_menu()
    userInput = input("Enter function you would like to perform: ")
    # if (userInput == "1"):

main()