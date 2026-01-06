import board
import neopixel
from my_utils import normalize_tree_coords, read_in_coords

def setup_tree(
    coords_file,
    num_pixels,
    brightness=0.5,
    auto_write=False
):
    # Load + normalize coordinates
    coords = read_in_coords(coords_file)
    # coords = normalize_tree_coords(coords)

    # Initialize NeoPixels
    pixels = neopixel.NeoPixel(
        board.D18,
        num_pixels,
        brightness=brightness,
        auto_write=auto_write
    )

    pixels.fill((0, 0, 0))
    pixels.show()

    return coords, pixels
