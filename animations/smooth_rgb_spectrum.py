import colorsys
from animations.animation import Animation

class SmoothRGBSpectrumAnimation(Animation):
    name = "Smooth RGB Spectrum"

    def setup(self):
        self.hue_speed = 0.02   # smaller = slower transition
        self.hue = 0.0

    def update(self, dt):
        # Convert hue -> RGB
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))

        self.pixels.fill(color)

        self.hue = (self.hue + self.hue_speed * dt) % 1.0