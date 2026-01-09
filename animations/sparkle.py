from animations.animation import Animation
import random
import math

class SparkleAnimation(Animation):
    name = "Sparkle"

    def setup(self):
        # Per-second constants (frame-rate independent)
        self.FADE_FACTOR = 0.85      # per-second fade multiplier (multiply color by this every 1s)
        self.SPAWN_CHANCE = 0.05     # spawn chance per second (probability a pixel spawns in 1s)
        self.colors = [(0, 0, 0)] * self.num_pixels

    def update(self, dt):
        if dt <= 0:
            return

        # Compute per-frame constants
        fade_per_frame = self.FADE_FACTOR ** dt
        spawn_chance_per_frame = 1 - (1 - self.SPAWN_CHANCE) ** dt

        for i in range(self.num_pixels):
            r, g, b = self.colors[i]

            # Fade existing color
            r = int(r * fade_per_frame)
            g = int(g * fade_per_frame)
            b = int(b * fade_per_frame)

            # Possibly spawn new sparkle
            if random.random() < spawn_chance_per_frame:
                r = random.randint(128, 255)
                g = random.randint(128, 255)
                b = random.randint(128, 255)

            self.colors[i] = (r, g, b)
            self.pixels[i] = (r, g, b)