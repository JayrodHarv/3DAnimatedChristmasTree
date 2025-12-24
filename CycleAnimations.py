import time
import random
import numpy as np
import board, neopixel
import TreeUtils

from animations import ANIMATIONS

# ===================================================
# LED SETUP
# ===================================================
COORDS_FILE = "tree_d_coords.txt"
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
coords = TreeUtils.read_in_coords(COORDS_FILE)

# ===================================================
# SCHEDULER LOOP
# ===================================================
MIN_DURATION = 1      # 1 Minute
MAX_DURATION = 3     # 3 Minutes

print("Tree animation scheduler running...")

try:
    while True:
        anim = random.choice(ANIMATIONS)
        duration = random.randint(MIN_DURATION * 3600, MAX_DURATION * 3600)

        print(f"Playing {anim.__name__} for {duration} minutes")
        anim(coords, pixels, duration)

        # small blackout between animations
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(2)

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")