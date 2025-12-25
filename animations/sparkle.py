import time
import random

def run(coords, pixels, duration):
    start_time = time.time()

    while time.time() - start_time < duration:
        for i in range(len(pixels)):
            if random.random() < 0.05:
                pixels[i] = (
                    random.randint(0,255),
                    random.randint(0,255),
                    random.randint(0,255)
                )
            else:
                pixels[i] = (0,0,0)

        pixels.show()
        time.sleep(0.05)