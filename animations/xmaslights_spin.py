import math
from animations.animation import Animation
from utils import color_manager

class XmasLightsSpinAnimation(Animation):
    name = "Xmas Lights Spin"

    def setup(self):
        self.angle = 0.0
        self.rotation_speed = math.pi  # radians per second

        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

        self.colorA = self.color_manager.next_color()
        self.colorB = self.color_manager.next_color()

    def update(self, dt):
        self.angle += self.rotation_speed * dt
        
        nx = 0.0
        ny = math.cos(self.angle)
        nz = math.sin(self.angle)

        cx, cy, cz = 0, 0, self.max_z / 2.0

        for i, (x, y, z) in enumerate(self.coords):
            dx = x - cx
            dy = y - cy
            dz = z - cz

            # Plane equation sign
            d = nx * dx + ny * dy + nz * dz

            self.pixels[i] = self.colorA if d >= 0 else self.colorB