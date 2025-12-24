import my_utils
import time

min_y, max_y = -30, 30

speed = 1.5

def run(coords, pixels, duration):
  start_time = time.time()
  num_pixels = len(coords)

  # main loop
  while time.time() - start_time < duration:

    # apply random rotation to tree
    rotated_coords = my_utils.randomly_rotate_tree(coords)

    turn_on_min, turn_on_max = -50, -30
    rand_color = my_utils.get_random_good_color()

    while turn_on_min < max_y and time.time() - start_time < duration:
      pixels.fill((0,0,0))

      turn_on_min += speed
      turn_on_max += speed

      for i in range(num_pixels):
        if turn_on_min <= rotated_coords[i][1] <= turn_on_max:
          pixels[i] = rand_color
          
      pixels.show()