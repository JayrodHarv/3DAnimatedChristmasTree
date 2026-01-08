from animations.animation import Animation
from utils import color_manager

class RandomRGBAllAnimation(Animation):
  name = "Random RGB All"

  def setup(self):
    self.color_manager = color_manager.ColorManager()
    self.color_manager.generate_pleasant_colors()
    self.color_manager.shuffle()
    self.hold_time = 3
    self.time_accumulator = 0
    self.current_color = self.color_manager.next_color()

  def update(self, dt):
    self.time_accumulator += dt

    if self.time_accumulator >= self.hold_time:
      self.time_accumulator = 0
      self.current_color = self.color_manager.next_color()

    for i in range(self.num_pixels):
      self.pixels[i] = self.current_color
