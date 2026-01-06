import board
import neopixel
from utils import my_utils

def setup_tree(
    coords_file,
    brightness=0.5,
    auto_write=False
):
    # Load + normalize coordinates
    coords = my_utils.read_in_coords(coords_file)
    # coords = normalize_tree_coords(coords)

    # Initialize NeoPixels
    pixels = neopixel.NeoPixel(
        board.D18,
        len(coords),
        brightness=brightness,
        auto_write=auto_write,
        pixel_order=neopixel.RGB
    )

    pixels.fill((0, 0, 0))
    pixels.show()

    return coords, pixels
