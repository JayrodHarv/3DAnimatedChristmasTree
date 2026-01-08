import numpy as np
from utils import color_manager
from animations.animation import Animation

class BreathingTreeAnimation(Animation):
    name = "Breathing Tree"

    def setup(self):
        # use accumulated dt instead of wall clock time
        self.time_accumulator = 0.0

        self.cm = color_manager.ColorManager()
        self.cm.generate_pleasant_colors()
        self.cm.shuffle()
        self.color = np.array(self.cm.next_color(), dtype=float)
        self.cycle_time = 6.0  # seconds per shrink + expand cycle

    def update(self, dt):
        # accumulate delta-time passed in by the runner
        self.time_accumulator += dt
        elapsed = self.time_accumulator

        # compute current scale 0–1 (shrinking and expanding)
        t = (elapsed * (2*np.pi / self.cycle_time)) % (2*np.pi)
        # sin wave from 0→1→0 pattern
        scale = (np.sin(t - np.pi/2) + 1) / 2   # smooth in/out between 0–1

        # when starting new expansion, pick new color
        # (detect near zero crossing of sin)
        if np.sin(t - np.pi/2) < -0.999:
            self.color = np.array(self.cm.next_color(), dtype=float)

        z_vals = np.array([p[2] for p in self.coords])
        z_min, z_max = np.min(z_vals), np.max(z_vals) + 100
        z_norm = (z_vals - z_min) / (z_max - z_min)   # 0–1 vertical height

        radii = np.sqrt(np.array([p[0] for p in self.coords])**2 +
                        np.array([p[1] for p in self.coords])**2)
        max_radius = np.max(radii) + 5

        # compute cone radius at each height for current scale
        # full tree radius profile = (1 - z_norm) * max_radius
        radius_profile = (1 - z_norm) * max_radius * scale

        # determine which LEDs are inside the current cone
        inside_mask = radii <= radius_profile

        # fade outer LEDs based on distance to boundary
        boundary_dist = np.clip((radius_profile - radii) / (0.05 * max_radius), 0, 1)

        brightness = inside_mask * boundary_dist

        # create RGB output
        colors = self.color[None, :] * brightness[:, None]
        colors = np.clip(colors, 0, 255).astype(np.uint8)

        # update LEDs
        for i in range(self.num_pixels):
            self.pixels[i] = tuple(colors[i])