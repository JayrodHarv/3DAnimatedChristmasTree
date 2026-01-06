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

    # Tree geometry
    zs = [z for _, _, z in coords]
    z_min = min(zs) # ~ -40
    z_max = max(zs) # ~ +40
    acc_for_error = 20
    height = abs(z_max) + abs(z_min) + acc_for_error

    max_radius = max(
        math.sqrt(x*x + y*y)
        for x, y, _ in coords
    ) + 10

    radial = [math.sqrt(x*x + y*y) for x, y, _ in coords]
    z_vals = zs

    # Animation parameters
    growth_speed = 0.6       # growth per second (0→1)
    spawn_interval = 3
    frame_delay = 0.03

    cones = []   # each: {"g": float, "color": (r,g,b)}
    last_spawn = start_time

    while duration is None or time.time() - start_time < duration:
        now = time.time()
        dt = now - last_frame_time
        last_frame_time = now

        # Spawn new cone
        if now - last_spawn >= spawn_interval:
            cones.append({
                "g": 0.0,
                "color": cm.next_color()
            })
            last_spawn = now

        # Grow cones
        for c in cones:
            c["g"] += growth_speed * dt

        # Remove cones that exceed full size
        cones = [c for c in cones if c["g"] <= 1.2]

        # Render
        for i in range(len(coords)):
            pixel_color = None

            for c in reversed(cones):  # newest wins
                z = z_vals[i]
                frac_height = (z - z_min) / height
                full_r = max_radius * (1 - frac_height)

                if radial[i] <= full_r * c["g"]:
                    pixel_color = c["color"]
                    break

            if pixel_color:
                pixels[i] = pixel_color

        pixels.show()
        time.sleep(frame_delay)
