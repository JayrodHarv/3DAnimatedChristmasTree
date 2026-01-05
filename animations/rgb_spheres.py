import time
import math
import random

def run(coords, pixels, duration = None):
    start_time = time.time()

    # Compute tree bounds once
    max_radius = 0
    for x, y, z in coords:
        r = math.sqrt(x*x + y*y + z*z)
        max_radius = max(max_radius, r)

    expansion_speed = max_radius / 60.0  # frames to fill tree
    frame_delay = 0.03

    while duration is None or time.time() - start_time < duration:
        # New sphere
        radius = 0.0
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        while radius <= max_radius:
            pixels.fill((0, 0, 0))

            for i, (x, y, z) in enumerate(coords):
                dist = math.sqrt(x*x + y*y + z*z)
                if dist <= radius:
                    pixels[i] = color

            pixels.show()
            radius += expansion_speed
            time.sleep(frame_delay)
