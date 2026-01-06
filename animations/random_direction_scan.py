from utils import my_utils
import time
import random

min_y, max_y = -30, 30

speed = 1.5

def run(coords, pixels, duration = None):
  start_time = time.time()
  num_pixels = len(coords)

  # main loop
  i = 0
  while duration is None or time.time() - start_time < duration:

    colors = my_utils.generate_pleasant_colors() # Get list of pleasant colors
    random.shuffle(colors) # Shuffle list of colors

    # apply random rotation to tree
    rotated_coords = my_utils.randomly_rotate_tree(coords)

    turn_on_min, turn_on_max = -50, -30
    # rand_color = my_utils.get_random_good_color()

    # Make sure that index doesn't go out of bounds of color list
    i = 0 if i > len(colors) - 1 else i + 1

    color = colors[i]

    while turn_on_min < max_y and (duration is None or time.time() - start_time < duration):
      pixels.fill((0,0,0))

      turn_on_min += speed
      turn_on_max += speed

      for i in range(num_pixels):
        if turn_on_min <= rotated_coords[i][1] <= turn_on_max:
          pixels[i] = color
          
      pixels.show()