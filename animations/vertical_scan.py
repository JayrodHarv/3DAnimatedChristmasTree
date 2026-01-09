from utils import color_manager
from animations.animation import Animation

class VerticalScanAnimation(Animation):
  name = "Vertical Scan"

  def setup(self):
    self.turn_on_min = 0
    self.turn_on_max = self.max_z / 10
    self.color_manager = color_manager.ColorManager()
    self.color_manager.generate_pleasant_colors()
    self.color_manager.shuffle()
    self.current_color = self.color_manager.next_color()

  def update(self, dt):
    speed = (self.max_z / 2) * dt  # units per second
    self.turn_on_min += speed
    self.turn_on_max += speed

    if self.turn_on_min > self.max_z:
      self.turn_on_min = 0
      self.turn_on_max = self.max_z / 10
      self.current_color = self.color_manager.next_color()

    for i in range(self.num_pixels):
      if self.turn_on_min <= self.coords[i][2] <= self.turn_on_max:
        self.pixels[i] = self.current_color
      else:
        self.pixels[i] = (0,0,0)