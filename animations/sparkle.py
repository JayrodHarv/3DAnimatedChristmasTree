import time
import random

def run(coords, pixels, duration):
    start_time = time.time()

    # Keep per-pixel color state (starts black)
    colors = [(0, 0, 0)] * len(pixels)

    FADE_FACTOR = 0.85      # how fast lights fade
    SPAWN_CHANCE = 0.05     # sparkle probability

    while time.time() - start_time < duration:
        for i in range(len(pixels)):

            # Spawn new sparkle
            if random.random() < SPAWN_CHANCE:
                colors[i] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            else:
                # Fade existing color
                r, g, b = colors[i]
                colors[i] = (
                    int(r * FADE_FACTOR),
                    int(g * FADE_FACTOR),
                    int(b * FADE_FACTOR)
                )

            pixels[i] = colors[i]

        pixels.show()
        time.sleep(0.05)