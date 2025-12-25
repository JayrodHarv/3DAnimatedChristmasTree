import time
import math
import colorsys
import numpy as np

def run(coords, pixels, duration = None):
    start_time = time.time()
    fps = 30

    coords = np.array(coords)
    x, y, z = coords[:,0], coords[:,1], coords[:,2]

    # Normalize coordinates
    z_norm = (z - z.min()) / (z.max() - z.min())
    radius = np.sqrt(x**2 + y**2)
    r_norm = radius / radius.max()

    while True:
        now = time.time()
        elapsed = now - start_time

        if duration is not None and elapsed >= duration:
            break

        for i in range(len(coords)):
            # Time distortion factors
            height_warp = 0.3 + z_norm[i]           # higher = faster
            radius_warp = 0.3 + r_norm[i] * 1.2     # outer = faster

            # Slow oscillation that modulates time itself
            warp_wave = 0.5 + 0.5 * math.sin(elapsed * 0.6 + z_norm[i] * 6)

            # Final effective time
            t = elapsed * height_warp * radius_warp * warp_wave

            # Color based on warped time
            hue = (t * 0.03 + z_norm[i]) % 1.0
            brightness = 0.6 + 0.4 * math.sin(t * 1.5)

            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, brightness)
            pixels[i] = (int(r * 255), int(g * 255), int(b * 255))

        pixels.show()
        time.sleep(1 / fps)