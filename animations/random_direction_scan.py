import my_utils
import board
import neopixel

num_pixels = 550

color_order = neopixel.RGB

pixels = neopixel.NeoPixel(board.D18, num_pixels, auto_write=False, pixel_order=color_order)

coords = my_utils.read_in_coords("tree_d_coords.txt")

min_y, max_y = -30, 30

speed = 1.5

try:
  print("Starting random plane sweep animation, Press ctrl+c to stop...")
  # main loop
  while True:

    # apply random rotation to tree
    rotated_coords = my_utils.randomly_rotate_tree(coords)

    turn_on_min, turn_on_max = -50, -30
    rand_color = my_utils.get_random_good_color()
    # rand_color = (random.randint(0,127), random.randint(0,127), random.randint(0,127))
    while turn_on_min < max_y:
      pixels.fill((0,0,0))

      turn_on_min += speed
      turn_on_max += speed

      for i in range(num_pixels):
        if turn_on_min <= rotated_coords[i][1] <= turn_on_max:
          pixels[i] = rand_color
      pixels.show()

except KeyboardInterrupt:
    print("\nStopping animation, clearing LEDs...")
    pixels.fill((0, 0, 0))
    pixels.show()
