import my_utils
import board
import neopixel
import time

min_y, max_y = -50, 50

speed = 1

def run(coords, pixels, duration):
  start_time = time.time()
  num_pixels = len(coords)

  # main loop
  while time.time() - start_time < duration:
    turn_on_min, turn_on_max = -70, -60
    rand_color = my_utils.get_random_good_color()
    
    while turn_on_min < max_y:
      pixels.fill((0,0,0))

      turn_on_min += speed
      turn_on_max += speed

      for i in range(num_pixels):
        if turn_on_min <= coords[i][1] <= turn_on_max:
          pixels[i] = rand_color

      pixels.show()