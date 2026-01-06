import time
import math
import random
from utils import my_utils

def run(coords, pixels, duration = None):
    start_time = time.time()
    last_frame_time = start_time

    colors = my_utils.generate_pleasant_colors() # Get list of pleasant colors
    random.shuffle(colors) # Shuffle list of colors

    distances = [
        math.sqrt(x*x + y*y + z*z)
        for x, y, z in coords
    ]
    max_radius = max(distances)

    expansion_speed = max_radius / 6.0   # units per second
    spawn_interval = 3                 # seconds
    frame_delay = 0.03

    spheres = []
    last_spawn = start_time

    i = 0
    while duration is None or time.time() - start_time < duration:
        now = time.time()
        dt = now - last_frame_time
        last_frame_time = now

        # Make sure that index doesn't go out of bounds of color list
        i = 0 if i > len(colors) - 1 else i + 1

        # Spawn new sphere
        if now - last_spawn >= spawn_interval:
            spheres.append({
                "radius": 0.0,
                "color": colors[i]
            })
            last_spawn = now

        # Grow spheres using elapsed time
        for s in spheres:
            s["radius"] += expansion_speed * dt

        # Cull old spheres
        spheres = [
            s for s in spheres
            if s["radius"] <= max_radius * 1.2
        ]

        # Update pixels
        for j, dist in enumerate(distances):
            pixel_color = None

            # iterate newest spheres first
            for s in reversed(spheres):
                if dist <= s["radius"]:
                    pixel_color = s["color"]
                    break

            if pixel_color:
                pixels[j] = pixel_color


        pixels.show()
        time.sleep(frame_delay)
