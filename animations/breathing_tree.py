import time
import numpy as np
import random
from utils import my_utils

FPS = 60

# cone shape parameters
MIN_SCALE = 0.0       # fully shrunk (0 = invisible)
MAX_SCALE = 1.0       # fully expanded
CYCLE_TIME = 6.0      # seconds per shrink + expand cycle

def run(coords, pixels, duration = None):
    start_time = time.time()
    NUM_LEDS = len(coords)

    coords -= np.mean(coords, axis=0)  # center the tree

    z_vals = coords[:, 2]
    z_min, z_max = np.min(z_vals), np.max(z_vals) + 20
    z_norm = (z_vals - z_min) / (z_max - z_min)   # 0–1 vertical height

    radii = np.sqrt(coords[:, 0]**2 + coords[:, 1]**2)
    max_radius = np.max(radii) + 5

    # ===================================================
    # ANIMATION LOOP
    # ===================================================

    frame_delay = 1.0 / FPS

    colors = my_utils.generate_pleasant_colors() # Get list of pleasant colors
    random.shuffle(colors) # Shuffle list of colors

    i = 0
    color = colors[i]
    while duration is None or time.time() - start_time < duration:
        # compute current scale 0–1 (shrinking and expanding)
        t = (time.time() * (2*np.pi / CYCLE_TIME)) % (2*np.pi)
        # sin wave from 0→1→0 pattern
        scale = (np.sin(t - np.pi/2) + 1) / 2   # smooth in/out between 0–1

        # when starting new expansion, pick new color
        # (detect near zero crossing of sin)
        if np.sin(t - np.pi/2) < -0.999:
            # Make sure that index doesn't go out of bounds of color list
            i = 0 if i > len(colors) - 1 else i + 1
            color = colors[i]

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
