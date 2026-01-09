import math
import random

from animations.animation import Animation

class EnchantmentGlintAnimation(Animation):
    name = "Minecraft Enchantment Glint"

    def setup(self):
        # Choose a random direction for the plane normal
        nx = random.gauss(0, 1)
        ny = random.gauss(0, 1)
        nz = random.gauss(0, 1)
        norm = math.sqrt(nx*nx + ny*ny + nz*nz)
        if norm == 0:
            nx, ny, nz = 0.0, 0.0, 1.0
            norm = 1.0
        self.normal = (nx / norm, ny / norm, nz / norm)

        # Precompute projections of all coordinates onto the normal
        self.projs = [self.normal[0]*x + self.normal[1]*y + self.normal[2]*z
                      for x, y, z in self.coords]

        self.min_p = min(self.projs)
        self.max_p = max(self.projs)
        self.range = self.max_p - self.min_p if self.max_p > self.min_p else 1.0

        # Plane thickness (controls visible band width)
        self.thickness = self.range / 6.0

        # Random speed so the plane crosses the tree in a few seconds
        crossing_seconds = random.uniform(4.0, 10.0)
        self.speed = (self.range + self.thickness * 2.0) / crossing_seconds
        # Randomize direction
        if random.choice([True, False]):
            self.speed *= -1.0

        # Initial offset (start somewhere within or slightly outside the tree projections)
        pad = 0.1 * self.range
        self.offset = random.uniform(self.min_p - pad, self.max_p + pad)

        # Purple color for the glint (can be tuned)
        self.color = (160, 64, 255)

    def update(self, dt):
        if dt <= 0:
            return

        # Move the plane
        self.offset += self.speed * dt

        # Loop the plane when it goes beyond the projection bounds
        pad = 0.1 * self.range
        if self.offset > self.max_p + self.thickness + pad:
            self.offset = self.min_p - self.thickness - pad
        if self.offset < self.min_p - self.thickness - pad:
            self.offset = self.max_p + self.thickness + pad

        # Compute per-pixel intensity based on distance from plane centerline
        half_thick = max(1e-6, self.thickness / 2.0)

        for j, (x, y, z) in enumerate(self.coords):
            proj = self.projs[j]
            d = proj - self.offset
            t = abs(d) / half_thick

            if t <= 1.0:
                # Smooth quadratic falloff for a soft glint
                falloff = 1.0 - (t * t)
                pr, pg, pb = self.color
                r = int(max(0, min(255, pr * falloff)))
                g = int(max(0, min(255, pg * falloff)))
                b = int(max(0, min(255, pb * falloff)))
                self.pixels[j] = (r, g, b)
            else:
                self.pixels[j] = (0, 0, 0)