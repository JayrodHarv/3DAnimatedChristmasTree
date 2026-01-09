from animations.animation import Animation
import random

class SparkleAnimation(Animation):
    name = "Sparkle"

    def setup(self):
        # Per-second constants (frame-rate independent)
        self.fade_factor = 0.85      # per-second fade multiplier (multiply color by this every 1s)
        self.spawn_chance = 0.05     # spawn chance per second (probability a pixel spawns in 1s)
        self.colors = [(0, 0, 0)] * self.num_pixels

    def update(self, dt):
        for i in range(self.num_pixels):

            # Spawn new sparkle
            if random.random() < self.spawn_chance:
                self.colors[i] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            else:
                # Fade existing color
                r, g, b = self.colors[i]
                self.colors[i] = (
                    int(r * self.fade_factor),
                    int(g * self.fade_factor),
                    int(b * self.fade_factor)
                )

            self.pixels[i] = self.colors[i]