import time
import random
import numpy as np
import board, neopixel
import TreeUtils

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
# IMPORT / DEFINE ANIMATIONS
# ===================================================
def random_direction_scan():
    return

def breathing_tree():
    return

def swirling_candy_cane():
    return

def rainbow_swirl():
    return

def scrolling_text():
    return

def fire():
    return

def vertical_scan():
    return

def xmaslights_spin():
    return

def enchantment_glint():
    return

# ===================================================
# ANIMATION REGISTRY
# ===================================================
ANIMATIONS = [
    random_direction_scan,
    breathing_tree,
    swirling_candy_cane,
    rainbow_swirl,
    scrolling_text,
    fire,
    vertical_scan,
    xmaslights_spin,
    enchantment_glint
]

# ===================================================
# SCHEDULER LOOP
# ===================================================
MIN_DURATION = 60      # seconds
MAX_DURATION = 180     # seconds

print("🎄 Tree animation scheduler running...")

try:
    while True:
        anim = random.choice(ANIMATIONS)
        duration = random.randint(MIN_DURATION, MAX_DURATION)

        print(f"▶ Playing {anim.__name__} for {duration}s")
        anim(pixels, coords, duration)

        # small blackout between animations
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(2)

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")