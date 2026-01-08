from animations.animation import Animation
from utils import color_manager

# HOLD_TIME = 3

# def run(coords, pixels, duration = None):
#   start_time = time.time()
#   num_pixels = len(coords)

#   cm = color_manager.ColorManager()
#   cm.generate_pleasant_colors()
#   cm.shuffle()

#   while duration is None or time.time() - start_time < duration:
    
#     color = cm.next_color()

#     for i in range(num_pixels):
#       pixels[i] = color
      
#     pixels.show()
#     time.sleep(HOLD_TIME)

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
