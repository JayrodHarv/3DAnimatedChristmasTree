import numpy as np
from utils import color_manager
from animations.animation import Animation

class SweepAnimation(Animation):
    name = "Sweep"

    def setup(self):
        # color management
        self.cm = color_manager.ColorManager()
        self.cm.generate_pleasant_colors()
        self.cm.shuffle()
        self.current_color = tuple(self.cm.next_color())

        # coordinates as array for fast dot products
        self.coords_arr = np.array(self.coords, dtype=float)

        # start with all pixels off (they'll retain colors as planes sweep)
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0)
        self.pixel_states = [(0, 0, 0) for _ in range(self.num_pixels)]

        # sweep timing and geometry
        self.sweep_time = 3.0  # seconds per full sweep
        self.thickness_fraction = 0.03  # slab thickness as fraction of projection range

        # pick initial direction and precompute projections
        self._choose_new_direction()

    def _choose_new_direction(self):
        # random unit normal
        v = np.random.normal(size=3)
        v /= np.linalg.norm(v)
        self.normal = v

        # projections of all points onto the normal
        self.projections = self.coords_arr.dot(self.normal)
        self.proj_min = float(np.min(self.projections))
        self.proj_max = float(np.max(self.projections))

        proj_range = self.proj_max - self.proj_min if self.proj_max != self.proj_min else 1.0
        # small margin so plane starts/ends outside the points
        self.margin = max(1.0, 0.02 * proj_range)
        self.start = self.proj_min - self.margin
        self.end = self.proj_max + self.margin

        # slab thickness (clamped to a reasonable minimum)
        self.thickness = max(self.thickness_fraction * proj_range, 1.0)

        # plane position and speed
        self.plane_pos = self.start
        self.speed = (self.end - self.start) / self.sweep_time

    def update(self, dt):
        # advance plane
        self.plane_pos += self.speed * dt

        # mark pixels whose projection lies within the current slab
        low = self.plane_pos - self.thickness / 2.0
        high = self.plane_pos + self.thickness / 2.0
        mask = (self.projections >= low) & (self.projections <= high)

        if mask.any():
            idxs = np.nonzero(mask)[0]
            for idx in idxs:
                self.pixel_states[idx] = self.current_color
                self.pixels[idx] = tuple(self.current_color)

        # when sweep completes, pick a new direction and color and continue
        if self.plane_pos > self.end:
            self.current_color = tuple(self.cm.next_color())
            self._choose_new_direction()
