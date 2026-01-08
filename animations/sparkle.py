from animations.animation import Animation
import random

class SparkleAnimation(Animation):
    name = "Sparkle"

    def setup(self):
        self.FADE_FACTOR = 0.85      # how fast lights fade
        self.SPAWN_CHANCE = 0.05     # sparkle probability
        self.colors = [(0, 0, 0)] * self.num_pixels

    def update(self, dt):
        for i in range(self.num_pixels):

            # Spawn new sparkle
            if random.random() < self.SPAWN_CHANCE:
                self.colors[i] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            else:
                # Fade existing color
                r, g, b = self.colors[i]
                self.colors[i] = (
                    int(r * self.FADE_FACTOR),
                    int(g * self.FADE_FACTOR),
                    int(b * self.FADE_FACTOR)
                )

            self.pixels[i] = self.colors[i]