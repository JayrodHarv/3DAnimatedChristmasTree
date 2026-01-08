import time
import numpy as np
from animations.animation import Animation

STRIPE_WIDTH = 7    # angular size of red/white bands (radians)
SPIRAL_TWIST = 4   # how tightly the spiral wraps around trunk

class SwirlingCandyCaneAnimation(Animation):
    name = "Swirling Candy Cane"

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

        # use accumulated dt instead of wall clock time
        self.time_accumulator = 0.0

    def update(self, dt):
        # accumulate delta time provided by runner
        self.time_accumulator += dt

        # Rotating phase term
        phase = self.time_accumulator * 2.0

        # Compute stripe pattern for each LED
        swirl_value = (self.theta + 2 * np.pi * SPIRAL_TWIST * self.z_norm + phase)
        stripe = ((swirl_value // STRIPE_WIDTH) % 2).astype(int)

        # Update LEDs
        for i in range(self.num_pixels):
            if stripe[i] == 0:
                self.pixels[i] = (255, 0, 0)   # Red
            else:
                self.pixels[i] = (255, 255, 255) # White