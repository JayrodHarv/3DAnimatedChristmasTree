import time
import math
import random
from utils import color_manager

def run(coords, pixels, duration = None):
    start_time = time.time()
    last_frame_time = start_time

    cm = color_manager.ColorManager()
    cm.generate_pleasant_colors()
    cm.shuffle()

    # Precompute geometry
    zs = [z for _, _, z in coords]
    z_top = max(zs)
    z_bottom = min(zs)
    height = z_top - z_bottom

    # Max radius of tree (base)
    max_radius = max(
        math.sqrt(x*x + y*y)
        for x, y, _ in coords
    )

    # Precompute per-pixel values
    radial_dist = [math.sqrt(x*x + y*y) for x, y, _ in coords]
    z_values = [z for _, _, z in coords]

    expansion_speed = height / 6.0   # units per second
    spawn_interval = 0.7
    frame_delay = 0.03

    cones = []   # each: {"z": float, "color": (r,g,b)}
    last_spawn = start_time

    while duration is None or time.time() - start_time < duration:
        now = time.time()
        dt = now - last_frame_time
        last_frame_time = now

        # Spawn new cone at the top
        if now - last_spawn >= spawn_interval:
            cones.append({
                "z": z_top,
                "color": cm.next_color()
            })
            last_spawn = now

        # Move cones downward
        for c in cones:
            c["z"] -= expansion_speed * dt

        # Remove cones below the tree
        cones = [
            c for c in cones
            if c["z"] >= z_bottom
        ]

        # Render
        for i in range(len(coords)):
            pixel_color = None

            # Newest cones win
            for c in reversed(cones):
                z = z_values[i]

                if z <= c["z"]:
                    # Compute cone radius at this height
                    frac = (c["z"] - z) / height
                    cone_r = max_radius * frac

                    if radial_dist[i] <= cone_r:
                        pixel_color = c["color"]
                        break

            if pixel_color:
                pixels[i] = pixel_color

        pixels.show()
        time.sleep(frame_delay)
