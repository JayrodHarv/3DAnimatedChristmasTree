import math
import colorsys
from animations.animation import Animation

class TimeWarpAnimation(Animation):
    name = "Time Warp"

    def setup(self):
        # use accumulated dt instead of wall clock time
        self.time_accumulator = 0.0

    def update(self, dt):
        # accumulate delta time provided by runner
        self.time_accumulator += dt
        elapsed = self.time_accumulator

        for j, (x, y, z) in enumerate(self.coords):
            # Normalize coordinates
            z_norm = (z - self.min_z) / (self.max_z if self.max_z != 0 else 1)
            radius = math.sqrt(x**2 + y**2)
            r_norm = radius / (self.radius if self.radius != 0 else 1)

            # Time distortion factors
            height_warp = 0.3 + z_norm           # higher = faster
            radius_warp = 0.3 + r_norm * 1.2     # outer = faster

            # Slow oscillation that modulates time itself
            warp_wave = 0.5 + 0.5 * math.sin(elapsed * 0.6 + z_norm * 6)

            # Final effective time
            t = elapsed * height_warp * radius_warp * warp_wave

            # Color based on warped time
            hue = (t * 0.03 + z_norm) % 1.0
            brightness = 0.6 + 0.4 * math.sin(t * 1.5)

            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, brightness)
            self.pixels[j] = (int(r * 255), int(g * 255), int(b * 255))