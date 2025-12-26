import sys
import random
import board, neopixel
from utils import my_utils
import time

from animations import ANIMATIONS

args = sys.argv[1:] # first argument is the name of script

COORDS_FILE = "tree_d_coords.txt" # set coords file as this by default

if (len(args) == 1):
    COORDS_FILE = args[0] # overiddes default coords file if provided

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

print("Tree animation scheduler running. Press ctrl+c to stop...")

try:
    while True:
        anim = random.choice(ANIMATIONS)
        duration = random.randint(MIN_DURATION, MAX_DURATION)

        print(f"Playing {anim['name']} for {duration} seconds")
        anim['function'](coords, pixels, duration)

        # small blackout between animations
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(0.5)

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")