import time
import numpy as np


# Plane animation parameters
NUM_PLANES = 2
THICKNESS = 8.0     # controls how wide the plane’s glow is
SPEED_RANGE = (0.5, 2)
FPS = 60

# Colors
PURPLE = np.array([255, 0, 255], dtype=float)
DARK = np.array([0, 0, 0], dtype=float)


def run(coords, pixels, duration = None):
    start_time = time.time()
    NUM_LEDS = len(coords)

    coords -= np.mean(coords, axis=0)  # center tree

    extent = np.max(np.ptp(coords, axis=0)) / 2

    # Generate random planes
    rng = np.random.default_rng()
    normals = rng.normal(size=(NUM_PLANES, 3))
    normals /= np.linalg.norm(normals, axis=1)[:, None]
    speeds = rng.uniform(*SPEED_RANGE, size=NUM_PLANES)
    offsets = rng.uniform(-extent, extent, size=NUM_PLANES)

    half_thick = THICKNESS / 2.0
    frame_delay = 1.0 / FPS

    # ===========================
    # MAIN ANIMATION LOOP
    # ===========================
    
    while duration is None or time.time() - start_time < duration:
        # Advance plane offsets
        offsets += speeds
        offsets = np.where(offsets > extent, -extent, offsets)

        # Compute signed distance of each LED to all planes
        distances = coords @ normals.T + offsets
        min_dist = np.min(np.abs(distances), axis=1)

        # Brightness 0–1
        brightness = np.clip(1.0 - (min_dist / half_thick), 0.0, 1.0)

        # Compute color per LED
        colors = DARK + (PURPLE - DARK) * brightness[:, None]
        colors = np.clip(colors, 0, 255).astype(np.uint8)

        # Update physical LEDs
        for i in range(NUM_LEDS):
            pixels[i] = tuple(colors[i])
        pixels.show()

        time.sleep(frame_delay)
