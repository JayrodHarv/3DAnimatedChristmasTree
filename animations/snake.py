import time
import random
from utils import my_utils

HOLD_TIME = 0.0005

def run(coords, pixels, duration = None):
  start_time = time.time()
  num_pixels = len(coords)

  colors = my_utils.generate_pleasant_colors() # Get list of pleasant colors
  random.shuffle(colors) # Shuffle list of colors

  ci = 0
  while duration is None or time.time() - start_time < duration:

    # Make sure that index doesn't go out of bounds of color list
    ci = 0 if ci > len(colors) - 1 else ci + 1

    color = colors[ci]
    for i in range(num_pixels):
      pixels[i] = color
      pixels.show()
      time.sleep(HOLD_TIME)