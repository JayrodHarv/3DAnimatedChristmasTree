import time
import numpy as np

FPS = 60
SPIN_SPEED = 0.5     # radians per frame
STRIPE_WIDTH = 7    # angular size of red/white bands (radians)
SPIRAL_TWIST = 4   # how tightly the spiral wraps around trunk

COLOR_RED   = np.array([127, 0, 0], dtype=float)
COLOR_WHITE = np.array([127, 127, 127], dtype=float)

def run(coords, pixels, duration):
    start_time = time.time()
    NUM_LEDS = len(coords)

    # Center and normalize
    coords -= np.mean(coords, axis=0)
    max_height = np.max(coords[:, 2]) - np.min(coords[:, 2])
    radius = np.max(np.linalg.norm(coords[:, [0,1]], axis=1))

    # Compute polar coordinates around Y-axis (treat Y as vertical)
    angles = np.arctan2(coords[:, 1], coords[:, 0])
    heights = (coords[:, 2] - np.min(coords[:, 2])) / max_height  # 0–1 normalized

    # =========================================================
    # ANIMATION LOOP
    # =========================================================
    
    frame_delay = 1.0 / FPS
    theta = 0.0

    while time.time() - start_time < duration:
        # For each LED, compute color from its polar angle + height
        phase = angles + heights * 2 * np.pi * SPIRAL_TWIST + theta
        # stripe pattern alternating every STRIPE_WIDTH radians
        stripe = ((phase // STRIPE_WIDTH) % 2).astype(int)

        colors = np.where(stripe[:, None] == 0, COLOR_RED, COLOR_WHITE)
        colors = np.clip(colors, 0, 255).astype(np.uint8)

        # send to LEDs
        for i in range(NUM_LEDS):
            pixels[i] = tuple(colors[i])
        pixels.show()

        # spin
        theta += SPIN_SPEED
        time.sleep(frame_delay)
