import time
import math
import random

def run(coords, pixels, duration = None):
    start_time = time.time()

    # Precompute distance of each pixel from center
    distances = [
        math.sqrt(x*x + y*y + z*z)
        for x, y, z in coords
    ]

    max_radius = max(distances)

    expansion_speed = max_radius / 80.0
    spawn_interval = 0.7  # seconds between new spheres
    frame_delay = 0.03

    spheres = []  # each = {"radius": float, "color": (r,g,b)}
    last_spawn = 0

    while duration is None or time.time() - start_time < duration:
        now = time.time()

        # Spawn new sphere
        if now - last_spawn >= spawn_interval:
            spheres.append({
                "radius": 0.0,
                "color": (
                    random.randint(60, 255),
                    random.randint(60, 255),
                    random.randint(60, 255),
                )
            })
            last_spawn = now

        # Grow all spheres
        for s in spheres:
            s["radius"] += expansion_speed

        # Remove spheres that are well past the tree
        spheres = [
            s for s in spheres
            if s["radius"] <= max_radius * 1.2
        ]

        # Update pixels
        for i, dist in enumerate(distances):
            pixel_color = None
            closest_delta = float("inf")

            for s in spheres:
                delta = abs(dist - s["radius"])
                if delta < closest_delta:
                    closest_delta = delta
                    pixel_color = s["color"]

            if pixel_color:
                pixels[i] = pixel_color

        pixels.show()
        time.sleep(frame_delay)
