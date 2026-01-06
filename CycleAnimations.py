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
        "--coords",
        nargs="?",
        default="normalized_tree_d_coords.txt",
        help="Path to coordinate file"
    )

    parser.add_argument(
        "--order",
        choices=["sequential", "random", "shuffle"],
        default="random",
        help="Animation play order"
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
MIN_DURATION = 30   # 30 seconds
MAX_DURATION = 180  # 3 minutes

def play_animation(anim, pixels, coords, duration):
    print(f"Playing {anim.name}")
    anim.run(coords, pixels, duration)

print("Tree animation scheduler running. Press ctrl+c to stop...")

try:
    while True:
        if args.order in ("random", "shuffle"):
            random.shuffle(animations)

        for anim in animations:
            duration = random.randint(MIN_DURATION, MAX_DURATION)
            play_animation(anim, pixels, coords, duration)

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")