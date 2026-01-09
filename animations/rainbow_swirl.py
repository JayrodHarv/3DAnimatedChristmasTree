import numpy as np
import colorsys
from animations.animation import Animation

class RainbowSwirlAnimation(Animation):
    name = "Rainbow Swirl"

    def setup(self):
        # Precompute normalized height and angle for each LED
        self.x = np.array([p[0] for p in self.coords])
        self.y = np.array([p[1] for p in self.coords])
        self.z = np.array([p[2] for p in self.coords])

        # Normalize vertical axis (z = height)
        z_min, z_max = self.z.min(), self.z.max()
        self.z_norm = (self.z - z_min) / (z_max - z_min)

        # Compute angle around trunk for each LED
        self.theta = np.arctan2(self.y, self.x)

    def update(self, dt):
        # Rotating phase term (ROTATION_SPEED = 2)
        phase = self.time_elapsed * 2.0

        # Compute rainbow hue for each LED
        swirl_value = (self.theta + 2 * np.pi * 0.5 * self.z_norm + phase) / (2 * np.pi)  # SPIRAL_TURNS
        hue = (swirl_value % 1.0)  # wrap 0–1

        # Convert to RGB colors
        colors = []
        for h in hue:
            r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)  # SATURATION, VALUE
            colors.append((
                int(r * 255),
                int(g * 255),
                int(b * 255)
            ))

        # Update LEDs
        for i in range(self.num_pixels):
            self.pixels[i] = tuple(colors[i])