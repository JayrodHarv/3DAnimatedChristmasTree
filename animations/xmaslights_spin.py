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

        # center point of the tree (use mean of points for robust center)
        xs = [p[0] for p in self.coords]
        ys = [p[1] for p in self.coords]
        zs = [p[2] for p in self.coords]
        self.center_x = sum(xs) / len(xs) if xs else 0.0
        self.center_y = sum(ys) / len(ys) if ys else 0.0
        self.center_z = sum(zs) / len(zs) if zs else 0.0

        # which axis to spin around: 'z' is vertical (default)
        self.spin_axis = 'z'

    def update(self, dt):
        # advance rotation
        # advance rotation (wrap using modulus)
        self.angle = (self.angle + self.rotation_speed * dt) % (2 * math.pi)

        # update colors only every color_change_interval seconds to avoid rapid flashing
        self.time_accumulator += dt
        if self.time_accumulator >= self.color_change_interval:
            self.colourA = self.color_manager.next_color()
            self.colourB = self.color_manager.next_color()
            self.time_accumulator = 0.0

        # make the rotating plane pass through the center of the tree (rotate about Z by default)
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        for i, (x, y, z) in enumerate(self.coords):
            dx = x - self.center_x
            dy = y - self.center_y

            # For rotation about Z axis: plane normal = (cos(angle), sin(angle), 0)
            # Points with dot >= 0 are on one side, < 0 on the other
            if (c * dx + s * dy) >= 0:
                self.pixels[i] = self.colourA
            else:
                self.pixels[i] = self.colourB