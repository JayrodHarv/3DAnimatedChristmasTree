import random
import board, neopixel
import my_utils

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
coords = my_utils.read_in_coords(COORDS_FILE)

print("Tree animation scheduler running...")

try:
    while True:
        print("Christmas Tree Animations:")
        i = 1
        for anim in ANIMATIONS:
            print("\t" + str(i) + ") " + anim['name'])
            i += 1

        try:
            number = int(input("Please select an animation to play by entering a number..."))

            if number - 1 < 0 or number - 1 > len(ANIMATIONS):
                raise ValueError
            
            anim = ANIMATIONS[number - 1]

            print(f"Playing {anim['name']}")
            anim['function'](coords, pixels)

            # small blackout between animations
            pixels.fill((0,0,0))
            pixels.show()

        except ValueError:
            print("You must enter a valid number. Please try again.")

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")