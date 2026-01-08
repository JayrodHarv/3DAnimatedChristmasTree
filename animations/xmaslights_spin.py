import math
from animations.animation import Animation
from utils import color_manager

class XmasLightsSpinAnimation(Animation):
    name = "Xmas Lights Spin"

    def setup(self):
        self.rotation_speed = 0.1
        self.angle = 0.0
        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

    def update(self, dt):
        self.angle += self.rotation_speed * dt
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

        colourA = self.color_manager.next_color()
        colourB = self.color_manager.next_color()

        for i, (x, y, z) in enumerate(self.coords):
            if math.tan(self.angle) * y <= z:
                self.pixels[i] = colourA
            else:
                self.pixels[i] = colourB