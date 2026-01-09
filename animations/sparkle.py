from animations.animation import Animation
import random
import math

class SparkleAnimation(Animation):
    name = "Sparkle"

    def setup(self):
        # Per-second constants (frame-rate independent)
        # fade_factor_per_sec: multiply color by this every 1 second (0 -> instant off, 1 -> no fade)
        self.fade_factor_per_sec = 0.25
        # spawn_rate_per_sec: expected number of spawns per pixel per second (small numbers)
        self.spawn_rate_per_sec = 0.1

        # Pre-allocate color state per pixel
        self.colors = [(0, 0, 0)] * self.num_pixels

    def update(self, dt):
        """Update colors using time delta `dt` (in seconds).

        This method is frame-rate independent: `dt` can be scaled by the
        Animation.run speed parameter to slow or speed up the effect.
        """
        if dt <= 0:
            return

        # Convert per-second constants into per-update values
        fade_multiplier = self.fade_factor_per_sec ** dt
        # Spawn modeled as Poisson process: probability at least one spawn in interval dt
        spawn_prob = 1.0 - math.exp(-self.spawn_rate_per_sec * dt)

        for i in range(self.num_pixels):
            # Spawn new sparkle (probability adjusted by dt)
            if random.random() < spawn_prob:
                self.colors[i] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            else:
                # Fade existing color using continuous-time multiplier
                r, g, b = self.colors[i]
                self.colors[i] = (
                    int(r * fade_multiplier),
                    int(g * fade_multiplier),
                    int(b * fade_multiplier)
                )

            self.pixels[i] = self.colors[i]