import math
from animations.animation import Animation
from utils import color_manager

class XmasLightsSpinAnimation(Animation):
    name = "Xmas Lights Spin"

    def setup(self):
        self.rotation_speed = 0.1
        self.angle = 0.0

        # timing for color updates (seconds)
        self.time_accumulator = 0.0
        self.color_change_interval = 0.8

        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

        # pick initial colors for two halves
        self.colourA = self.color_manager.next_color()
        self.colourB = self.color_manager.next_color()

    def update(self, dt):
        # advance rotation
        self.angle += self.rotation_speed * dt
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

        # update colors only every color_change_interval seconds to avoid rapid flashing
        self.time_accumulator += dt
        if self.time_accumulator >= self.color_change_interval:
            self.colourA = self.color_manager.next_color()
            self.colourB = self.color_manager.next_color()
            self.time_accumulator = 0.0

        # make the rotating plane pass through the center of the tree
        center_x = (self.min_x + self.max_x) / 2.0
        center_y = (self.min_y + self.max_y) / 2.0
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        for i, (x, y, z) in enumerate(self.coords):
            dx = x - center_x
            dy = y - center_y
            # dot product with unit normal defines which side of the plane the point is on
            if c * dx + s * dy >= 0:
                self.pixels[i] = self.colourA
            else:
                self.pixels[i] = self.colourB