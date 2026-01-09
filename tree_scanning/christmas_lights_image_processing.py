import cv2
import sys

def load_image(light_num, folderPath):
    # Load the image
    return cv2.imread(f'{folderPath}/({light_num}).jpg')

def get_brightest_point(light_num, folderPath, display=False):

    image = load_image(light_num, folderPath)
    if image is None:
        raise FileNotFoundError(f"Image for light {light_num} not found in {folderPath}")

    height, width = image.shape[:2]

    # Compute horizontal crop using the same relative padding as before (600/1920)
    rel_pad = 600 / 1920
    pad_x = int(round(width * rel_pad))

    x_start = pad_x
    x_end = width - pad_x
    y_start = 0
    y_end = height

    # Ensure we don't create invalid slices
    x_start = max(0, min(x_start, width - 1))
    x_end = max(x_start + 1, min(x_end, width))
    y_start = max(0, min(y_start, height - 1))
    y_end = max(y_start + 1, min(y_end, height))

    cropped_image = image[y_start:y_end, x_start:x_end]

    # Convert the image to grayscale for easier processing
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Scale blur kernel with image size for consistent behavior on different resolutions
    # Kernel size must be positive and odd
    base_kernel = 41
    scale = max(1.0, height / 1080)
    k = int(round(base_kernel * scale))
    if k % 2 == 0:
        k += 1

    blurred_image = cv2.GaussianBlur(gray_image, (k, k), 0)

    # Find the minimum and maximum pixel values and their locations
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(blurred_image)

    # max_loc is relative to the cropped image; convert to full-image coordinates
    brightest_pixel_coordinates = (max_loc[0] + x_start, max_loc[1] + y_start)

    if display:
        # Draw a circle on the cropped image for visualization
        cv2.circle(cropped_image, max_loc, max(2, k // 8), (0, 0, 255), 2)
        cv2.imshow('Image with Brightest Pixel', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return brightest_pixel_coordinates

def get_upright_coord(coord, image_height=None):
    """Return coordinates with flipped Y axis (image origin at top-left -> origin at bottom-left).

    If image_height is None, we assume 1080 for backwards compatibility, but it's
    recommended to pass the actual image height.
    """
    if image_height is None:
        image_height = 1080

    return [coord[0], image_height - coord[1]]

def generateCoordinatesFromImages(numImages, folderPath, name, display=False):
    """Gather 2D coordinates for images in a folder, returning upright coordinates
    (with origin at bottom-left). This works for any image dimensions.
    """
    coords = []
    for i in range(0, numImages):
        # Request image size along with coordinate so we can flip Y correctly
        coord = get_brightest_point(i + 1, folderPath)
        coords.append(coord)

        # Progress Bar
        percent = int((i + 1) / numImages * 100)
        bar = "#" * (percent // 2) + "-" * (50 - percent // 2)

        sys.stdout.write(f"\rGathering 2D coordinates from {name} images: [{bar}] {percent}%")
        sys.stdout.flush()

    print(" Done!")

    if display:
        # Display coordinates using matplotlib
        import matplotlib.pyplot as plt
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        plt.scatter(xs, ys)
        plt.title(f"2D Coordinates from {name} Images")
        plt.xlabel("X (pixels)")
        plt.ylabel("Y (pixels)")
        # flip Y axis for display
        plt.ylim(plt.ylim()[::-1])
        plt.show()

    return coords