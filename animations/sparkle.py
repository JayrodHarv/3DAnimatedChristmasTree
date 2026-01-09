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
        # Convert per-second constants into per-update values
        if dt <= 0:
            return

        fade_multiplier = self.FADE_FACTOR ** dt
        # Model spawns as a Poisson process: probability at least one spawn in interval dt
        spawn_prob = 1 - math.exp(-self.SPAWN_CHANCE * dt)

        for i in range(self.num_pixels):
            # Spawn new sparkle (probability adjusted by dt)
            if random.random() < spawn_prob:
                self.colors[i] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            else:
                # Fade existing color
                r, g, b = self.colors[i]
                self.colors[i] = (
                    int(r * fade_multiplier),
                    int(g * fade_multiplier),
                    int(b * fade_multiplier)
                )

            self.pixels[i] = self.colors[i]