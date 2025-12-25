import time
import numpy as np
import colorsys

FPS = 60

# swirl parameters
SPIRAL_TURNS = 0.5      # number of vertical wraps around tree
ROTATION_SPEED = 2    # radians per second
Z_SCALE = 3           # how much z affects color swirl tightness
SATURATION = 1.0        # 0–1 color saturation
VALUE = 1.0             # 0–1 brightness


def run(coords, pixels, duration = None):
    NUM_LEDS = len(coords)

    coords -= np.mean(coords, axis=0)  # center tree

    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]

    # Normalize vertical axis (z = height)
    z_min, z_max = z.min(), z.max()
    z_norm = (z - z_min) / (z_max - z_min)

    # Compute angle around trunk for each LED
    theta = np.arctan2(y, x)

    # ===================================================
    # HELPER: HSV to RGB (0–255)
    # ===================================================
    def hsv_to_rgb(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    # ===================================================
    # ANIMATION LOOP
    # ===================================================

    frame_delay = 1.0 / FPS
    start_time = time.time()

    while duration is None or time.time() - start_time < duration:
        t = time.time() - start_time

        # Rotating phase term
        phase = t * ROTATION_SPEED

        # Compute rainbow hue for each LED
        # Combine angle + height + time for swirling motion
        swirl_value = (theta + 2 * np.pi * SPIRAL_TURNS * z_norm + phase) / (2 * np.pi)
        hue = (swirl_value % 1.0)  # wrap 0–1

        # Convert to RGB colors
        colors = np.array([hsv_to_rgb(h, SATURATION, VALUE) for h in hue])

        # Update LEDs
        for i in range(NUM_LEDS):
            pixels[i] = tuple(colors[i])
        pixels.show()

        time.sleep(frame_delay)
