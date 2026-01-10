import numpy as np
from utils import color_manager
from animations.animation import Animation

class GradientSweepAnimation(Animation):
    name = "Gradient Sweep"

    def setup(self):
        # color management (choose two endpoints for the gradient)
        self.cm = color_manager.ColorManager()
        self.cm.generate_pleasant_colors()
        self.cm.shuffle()
        self.color_a = np.array(self.cm.next_color(), dtype=float)
        self.color_b = np.array(self.cm.next_color(), dtype=float)

        # coords array for fast projection math
        self.coords_arr = np.array(self.coords, dtype=float)

        # persistent pixel colors (start dark)
        self.pixel_states = [ (0, 0, 0) for _ in range(self.num_pixels) ]
        for i in range(self.num_pixels):
            self.pixels[i] = self.pixel_states[i]

        # sweep geometry and timing
        self.sweep_time = 3.0  # seconds for a full sweep
        self.thickness_fraction = 0.03  # slab thickness relative to projection range

        # pick initial random direction
        self._choose_new_direction()

    def _choose_new_direction(self):
        v = np.random.normal(size=3)
        v /= np.linalg.norm(v)
        self.normal = v

        self.projections = self.coords_arr.dot(self.normal)
        self.proj_min = float(np.min(self.projections))
        self.proj_max = float(np.max(self.projections))

        proj_range = self.proj_max - self.proj_min if self.proj_max != self.proj_min else 1.0
        self.margin = max(1.0, 0.02 * proj_range)
        self.start = self.proj_min - self.margin
        self.end = self.proj_max + self.margin

        self.thickness = max(self.thickness_fraction * proj_range, 1.0)
        self.plane_pos = self.start
        self.speed = (self.end - self.start) / self.sweep_time

        # pick new gradient endpoints for this sweep
        self.color_a = np.array(self.cm.next_color(), dtype=float)
        self.color_b = np.array(self.cm.next_color(), dtype=float)

    def update(self, dt):
        # advance plane
        self.plane_pos += self.speed * dt

        # slab bounds
        low = self.plane_pos - self.thickness / 2.0
        high = self.plane_pos + self.thickness / 2.0

        # indices in slab
        mask = (self.projections >= low) & (self.projections <= high)
        if mask.any():
            idxs = np.nonzero(mask)[0]
            proj_range = self.proj_max - self.proj_min if self.proj_max != self.proj_min else 1.0
            for idx in idxs:
                # normalized position across the whole projection range (not just slab)
                frac = (self.projections[idx] - self.proj_min) / proj_range
                frac = np.clip(frac, 0.0, 1.0)
                color = (1.0 - frac) * self.color_a + frac * self.color_b
                color = np.clip(color, 0, 255).astype(np.uint8)
                self.pixel_states[idx] = tuple(color)
                self.pixels[idx] = tuple(color)

        # when completed a sweep, pick a new direction and gradient
        if self.plane_pos > self.end:
            self._choose_new_direction()
