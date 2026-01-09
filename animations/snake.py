from utils import color_manager
from animations.animation import Animation

class SnakeAnimation(Animation):
  name = "Snake"

  def setup(self):
    self.color_manager = color_manager.ColorManager()
    self.color_manager.generate_pleasant_colors()
    self.color_manager.shuffle()
    self.current_color = self.color_manager.next_color()
    self.current_index = 0

  def update(self, dt):
    speed = 0.05  # seconds per pixel

    while self.time_elapsed >= speed:
      self.time_elapsed -= speed

      # Set current pixel to current color
      self.pixels[self.current_index] = self.current_color

      # Move to next pixel
      self.current_index += 1

      if self.current_index >= self.num_pixels:
        # Reset to start
        self.current_index = 0
        self.current_color = self.color_manager.next_color()
        # Clear pixels for new snake
        for i in range(self.num_pixels):
          self.pixels[i] = (0, 0, 0)