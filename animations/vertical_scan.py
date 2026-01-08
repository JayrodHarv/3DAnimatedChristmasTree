from utils import my_utils, color_manager
from animations.animation import Animation
import time

# def run(coords, pixels, duration = None):
#   start_time = time.time()
#   num_pixels = len(coords)

#   cm = color_manager.ColorManager()
#   cm.generate_pleasant_colors()
#   cm.shuffle()

#   # main loop
#   while duration is None or time.time() - start_time < duration:
#     turn_on_min, turn_on_max = -70, -60

#     color = cm.next_color()
    
#     while turn_on_min < max_y:
#       pixels.fill((0,0,0))

#       turn_on_min += speed
#       turn_on_max += speed

#       for i in range(num_pixels):
#         if turn_on_min <= coords[i][2] <= turn_on_max:
#           pixels[i] = color

#       pixels.show()


class VerticalScanAnimation(Animation):
  name = "Vertical Scan"

  def setup(self):
    self.turn_on_min = 0
    self.turn_on_max = 100
    self.color_manager = color_manager.ColorManager()
    self.color_manager.generate_pleasant_colors()
    self.color_manager.shuffle()
    self.current_color = self.color_manager.next_color()

  def update(self, dt):
    speed = 200 * dt  # units per second
    self.turn_on_min += speed
    self.turn_on_max += speed

    if self.turn_on_min > self.max_z:
      self.turn_on_min = 0
      self.turn_on_max = 100
      self.current_color = self.color_manager.next_color()

    for i in range(self.num_pixels):
      if self.turn_on_min <= self.coords[i][2] <= self.turn_on_max:
        self.pixels[i] = self.current_color
      else:
        self.pixels[i] = (0,0,0)