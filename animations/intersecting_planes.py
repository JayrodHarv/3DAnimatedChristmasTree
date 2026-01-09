import math
import random

from animations.animation import Animation
from utils import color_manager


class IntersectingPlanesAnimation(Animation):
    name = "Intersecting Planes"

    def setup(self):
        # Configuration
        self.num_planes = 4
        self.wrap_padding = 0.1  # padding when wrapping planes beyond bounds

        # Prepare colors for the planes
        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors(self.num_planes)
        self.color_manager.shuffle()

        # Create planes with random normals, speeds and initial offsets
        self.planes = []

        for i in range(self.num_planes):
            # Random unit normal
            nx = random.gauss(0, 1)
            ny = random.gauss(0, 1)
            nz = random.gauss(0, 1)
            norm = math.sqrt(nx*nx + ny*ny + nz*nz)
            if norm == 0:
                nx, ny, nz = 1.0, 0.0, 0.0
                norm = 1.0
            nx, ny, nz = nx / norm, ny / norm, nz / norm

            # Project all coordinates onto the normal to find movement bounds
            projs = [nx*x + ny*y + nz*z for x, y, z in self.coords]
            min_p, max_p = min(projs), max(projs)
            proj_range = max_p - min_p if max_p > min_p else 1.0

            # Thickness relative to projection range
            thickness = proj_range / 6.0

            # Speed chosen so plane crosses tree in a few seconds (random dir)
            speed = random.choice([-1.0, 1.0]) * proj_range / random.uniform(4.0, 12.0)

            # Initial offset somewhere in the projection span
            offset = random.uniform(min_p - self.wrap_padding * proj_range,
                                     max_p + self.wrap_padding * proj_range)

            color = self.color_manager.next_color()

            self.planes.append({
                "normal": (nx, ny, nz),
                "projs": projs,
                "min": min_p,
                "max": max_p,
                "range": proj_range,
                "thickness": thickness,
                "speed": speed,
                "offset": offset,
                "color": color
            })

    def update(self, dt):
        if dt <= 0:
            return

        # Move planes and wrap around bounds
        for p in self.planes:
            p["offset"] += p["speed"] * dt

            # wrap forward
            if p["offset"] > p["max"] + p["thickness"] + p.get("range", 0) * self.wrap_padding:
                p["offset"] = p["min"] - p["thickness"] - p.get("range", 0) * self.wrap_padding

            # wrap backward
            if p["offset"] < p["min"] - p["thickness"] - p.get("range", 0) * self.wrap_padding:
                p["offset"] = p["max"] + p["thickness"] + p.get("range", 0) * self.wrap_padding

        # For each pixel, accumulate contributions from all planes
        for j, (x, y, z) in enumerate(self.coords):
            r_acc = 0.0
            g_acc = 0.0
            b_acc = 0.0

            for p in self.planes:
                proj = p["projs"][j]
                d = proj - p["offset"]

                # Compute falloff (smooth, quadratic); plane is centered at offset
                half_thick = max(1e-6, p["thickness"] / 2.0)
                t = abs(d) / half_thick
                if t <= 1.0:
                    # smooth falloff: 1 - t^2 gives a soft edge
                    falloff = 1.0 - (t * t)
                else:
                    falloff = 0.0

                if falloff > 0.0:
                    pr, pg, pb = p["color"]
                    r_acc += pr * falloff
                    g_acc += pg * falloff
                    b_acc += pb * falloff

            # Cap color values to 0-255 and assign
            r = int(max(0, min(255, r_acc)))
            g = int(max(0, min(255, g_acc)))
            b = int(max(0, min(255, b_acc)))

            # If no plane contributed, leave the pixel as black (0,0,0)
            self.pixels[j] = (r, g, b)
