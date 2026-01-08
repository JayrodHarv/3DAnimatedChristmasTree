from utils import color_manager
from animations.animation import Animation

class SnakeAnimation(Animation):
  name = "Snake"

  def setup(self):
    self.color_manager = color_manager.ColorManager()
    self.color_manager.generate_pleasant_colors()
    self.color_manager.shuffle()
    self.hold_time = 0.0005
    self.current_color = self.color_manager.next_color()
    self.current_index = 0
    self.time_accumulator = 0

  def update(self, dt):
    self.time_accumulator += dt

    if self.time_accumulator >= self.hold_time:
      self.time_accumulator = 0

      # Set current pixel to color
      self.pixels[self.current_index] = self.current_color

      # Move to next pixel
      self.current_index += 1

      if self.current_index >= self.num_pixels:
        self.current_index = 0
        self.current_color = self.color_manager.next_color()