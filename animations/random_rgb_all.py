import time
import random
from utils import color_manager

HOLD_TIME = 3

def run(coords, pixels, duration = None):
  start_time = time.time()
  num_pixels = len(coords)

  cm = color_manager.ColorManager()
  cm.generate_pleasant_colors()
  cm.shuffle()

  while duration is None or time.time() - start_time < duration:
    
    color = cm.next_color()

    for i in range(num_pixels):
      pixels[i] = color
      
    pixels.show()
    time.sleep(HOLD_TIME)
