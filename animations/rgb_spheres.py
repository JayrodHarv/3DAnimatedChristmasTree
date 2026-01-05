import time
import math
import random
from utils import my_utils

def run(coords, pixels, duration = None):

    # NORMALIZE COORDS
    coords = my_utils.normalize_tree_coords(coords)

    start_time = time.time()
    last_frame_time = start_time

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

    while duration is None or time.time() - start_time < duration:
        now = time.time()
        dt = now - last_frame_time
        last_frame_time = now

        # Spawn new sphere
        if now - last_spawn >= spawn_interval:
            spheres.append({
                "radius": 0.0,
                "color": my_utils.get_random_good_color()
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
        for i, dist in enumerate(distances):
            pixel_color = None

            # iterate newest spheres first
            for s in reversed(spheres):
                if dist <= s["radius"]:
                    pixel_color = s["color"]
                    break

            if pixel_color:
                pixels[i] = pixel_color


        pixels.show()
        time.sleep(frame_delay)
