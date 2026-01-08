from animations.animation import Animation
import random

# def run(coords, pixels, duration = None):
#     start_time = time.time()

#     # Keep per-pixel color state (starts black)
#     colors = [(0, 0, 0)] * len(pixels)

#     FADE_FACTOR = 0.85      # how fast lights fade
#     SPAWN_CHANCE = 0.05     # sparkle probability

#     while duration is None or time.time() - start_time < duration:
#         for i in range(len(pixels)):

#             # Spawn new sparkle
#             if random.random() < SPAWN_CHANCE:
#                 colors[i] = (
#                     random.randint(0, 255),
#                     random.randint(0, 255),
#                     random.randint(0, 255)
#                 )
#             else:
#                 # Fade existing color
#                 r, g, b = colors[i]
#                 colors[i] = (
#                     int(r * FADE_FACTOR),
#                     int(g * FADE_FACTOR),
#                     int(b * FADE_FACTOR)
#                 )

#             pixels[i] = colors[i]

#         pixels.show()
#         time.sleep(0.05)

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