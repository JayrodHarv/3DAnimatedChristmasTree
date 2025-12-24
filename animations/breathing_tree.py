import time
import numpy as np
import board, neopixel
import random
import my_utils

# ===================================================
# USER SETTINGS
# ===================================================
NUM_LEDS = 550
PIXEL_PIN = board.D18
ORDER = neopixel.RGB
BRIGHTNESS = 0.5
FPS = 60

# cone shape parameters
MIN_SCALE = 0.0       # fully shrunk (0 = invisible)
MAX_SCALE = 1.0       # fully expanded
CYCLE_TIME = 6.0      # seconds per shrink + expand cycle

# ===================================================
# INIT NEOPIXELS
# ===================================================
pixels = neopixel.NeoPixel(
    PIXEL_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False, pixel_order=ORDER
)

# ===================================================
# LOAD AND NORMALIZE LED POSITIONS
# ===================================================
coords = my_utils.read_in_coords("tree_d_coords.txt")
coords -= np.mean(coords, axis=0)  # center the tree

z_vals = coords[:, 2]
z_min, z_max = np.min(z_vals), np.max(z_vals) + 20
z_norm = (z_vals - z_min) / (z_max - z_min)   # 0–1 vertical height

radii = np.sqrt(coords[:, 0]**2 + coords[:, 1]**2)
max_radius = np.max(radii) + 5

# ===================================================
# ANIMATION LOOP
# ===================================================
print("Playing Breathing Tree Animation")

frame_delay = 1.0 / FPS
phase = 0.0
direction = 1.0
color = np.array([random.randint(0,255), random.randint(0,255), random.randint(0,255)], dtype=float)

try:
    while True:
        # compute current scale 0–1 (shrinking and expanding)
        t = (time.time() * (2*np.pi / CYCLE_TIME)) % (2*np.pi)
        # sin wave from 0→1→0 pattern
        scale = (np.sin(t - np.pi/2) + 1) / 2   # smooth in/out between 0–1

        # when starting new expansion, pick new color
        # (detect near zero crossing of sin)
        if np.sin(t - np.pi/2) < -0.999:
            color = np.array([random.randint(0,255),
                              random.randint(0,255),
                              random.randint(0,255)], dtype=float)

        # compute cone radius at each height for current scale
        # full tree radius profile = (1 - z_norm) * max_radius
        radius_profile = (1 - z_norm) * max_radius * scale

        # determine which LEDs are inside the current cone
        inside_mask = radii <= radius_profile

        # fade outer LEDs based on distance to boundary
        boundary_dist = np.clip((radius_profile - radii) / (0.05 * max_radius), 0, 1)

        brightness = inside_mask * boundary_dist

        # create RGB output
        colors = color[None, :] * brightness[:, None]
        colors = np.clip(colors, 0, 255).astype(np.uint8)

        # update LEDs
        for i in range(NUM_LEDS):
            pixels[i] = tuple(colors[i])
        pixels.show()

        time.sleep(frame_delay)

except KeyboardInterrupt:
    pixels.fill((0,0,0))
    pixels.show()
    print("\nStopped.")
