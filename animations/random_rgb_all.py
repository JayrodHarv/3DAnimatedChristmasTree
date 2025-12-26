import time
import random

HOLD_TIME = 3

def run(coords, pixels, duration = None):
  start_time = time.time()
  num_pixels = len(coords)

  while duration is None or time.time() - start_time < duration:
    rand_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) 
    for i in range(num_pixels):
      pixels[i] = rand_color
      
    pixels.show()
    time.sleep(HOLD_TIME)
