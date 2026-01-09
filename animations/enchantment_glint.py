import math
import random

import math
import random

from animations.animation import Animation


class EnchantmentGlintAnimation(Animation):
    name = "Minecraft Enchantment Glint"

    def setup(self):
        # Configuration: allow two simultaneous glint planes
        self.num_planes = 2
        self.base_color = (160, 64, 255)  # purple

        # Maintain a list of active planes
        self.planes = []
        for _ in range(self.num_planes):
            self.planes.append(self._spawn_plane(initial=True))

    def _spawn_plane(self, initial=False):
        # Random unit normal
        nx = random.gauss(0, 1)
        ny = random.gauss(0, 1)
        nz = random.gauss(0, 1)
        norm = math.sqrt(nx*nx + ny*ny + nz*nz)
        if norm == 0:
            nx, ny, nz = 0.0, 0.0, 1.0
            norm = 1.0
        normal = (nx / norm, ny / norm, nz / norm)

        # Projections onto normal
        projs = [normal[0]*x + normal[1]*y + normal[2]*z for x, y, z in self.coords]
        min_p = min(projs)
        max_p = max(projs)
        proj_range = max_p - min_p if max_p > min_p else 1.0

        # Thickness and speed
        thickness = proj_range / 6.0
        crossing_seconds = random.uniform(2.0, 5.0)
        speed = (proj_range + thickness * 2.0) / crossing_seconds
        if random.choice([True, False]):
            speed *= -1.0

        pad = 0.1 * proj_range
        if initial:
            offset = random.uniform(min_p - pad, max_p + pad)
        else:
            # spawn outside on side opposite movement so it moves through the tree
            if speed > 0:
                offset = min_p - thickness - pad
            else:
                offset = max_p + thickness + pad

        return {
            "normal": normal,
            "projs": projs,
            "min": min_p,
            "max": max_p,
            "range": proj_range,
            "thickness": thickness,
            "speed": speed,
            "offset": offset,
            "color": self.base_color
        }

    def update(self, dt):
        if dt <= 0:
            return

        # Move planes and respawn with new random direction when they exit bounds
        for i, p in enumerate(self.planes):
            p["offset"] += p["speed"] * dt

            wrap_pad = p["range"] * 0.1
            if p["offset"] > p["max"] + p["thickness"] + wrap_pad or p["offset"] < p["min"] - p["thickness"] - wrap_pad:
                # respawn this plane with a new random direction and speed
                self.planes[i] = self._spawn_plane(initial=False)

        # Render: additive blending where planes overlap
        for j, (x, y, z) in enumerate(self.coords):
            r_acc = 0.0
            g_acc = 0.0
            b_acc = 0.0

            for p in self.planes:
                proj = p["projs"][j]
                d = proj - p["offset"]

                half_thick = max(1e-6, p["thickness"] / 2.0)
                t = abs(d) / half_thick
                if t <= 1.0:
                    falloff = 1.0 - (t * t)
                    pr, pg, pb = p["color"]
                    r_acc += pr * falloff
                    g_acc += pg * falloff
                    b_acc += pb * falloff

            r = int(max(0, min(255, r_acc)))
            g = int(max(0, min(255, g_acc)))
            b = int(max(0, min(255, b_acc)))

            self.pixels[j] = (r, g, b)