import sys
import random
import board, neopixel
from utils import my_utils
import time
import argparse

from animations import ANIMATIONS

COORDS_FILE = "normalized_tree_d_coords.txt" # set coords file as this by default

ORDER = "random" # Random order by default

def parse_args():
    parser = argparse.ArgumentParser(
        description="3D Christmas Tree Animation Scheduler"
    )

    parser.add_argument(
        "--order",
        choices=["in-order", "shuffle"],
        default="random",
        help="Animation play order"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default="60",
        help="Duration that each animation plays for"
    )

    parser.add_argument(
        "--coords",
        nargs="?",
        default="normalized_tree_d_coords.txt",
        help="Path to coordinate file"
    )

    return parser.parse_args()

args = parse_args()

animations = ANIMATIONS[:]  # copy list

# ===================================================
# LED SETUP
# ===================================================
NUM_LEDS = 550
PIXEL_PIN = board.D18
ORDER = neopixel.RGB
BRIGHTNESS = 0.5

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_LEDS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=ORDER
)

# ===================================================
# LOAD COORDINATES
# ===================================================
coords = my_utils.read_in_coords(COORDS_FILE)

# ===================================================
# SCHEDULER LOOP
# ===================================================

def play_animation(anim, pixels, coords, duration):
    print(f"Playing {anim['name']} for {duration} seconds")
    anim['function'](coords, pixels, duration)

print("Tree animation scheduler running. Press ctrl+c to stop...")

try:
    while True:
        if args.order == "shuffle":
            random.shuffle(animations)

        for anim in animations:
            play_animation(anim, pixels, coords, args.duration)

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")