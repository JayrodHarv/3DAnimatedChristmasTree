import numpy as np
from utils import color_manager
from animations.animation import Animation

class BreathingTreeAnimation(Animation):
    name = "Breathing Tree"

    def setup(self):
        self.cm = color_manager.ColorManager()
        self.cm.generate_pleasant_colors()
        self.cm.shuffle()
        self.color = np.array(self.cm.next_color(), dtype=float)

        # cycle controls how fast the cone grows/shrinks
        self.cycle_time = 6.0  # seconds per shrink + expand cycle

        # growth factor range (fraction of `self.radius` used)
        self.growth_min = 0.2
        self.growth_max = 2.0

        # how quickly the cone's edge fades (as fraction of radius)
        self.boundary_fraction = 0.05

        # small offset above the highest LED so the cone tip sits slightly above the tree
        # (helps ensure top LEDs can be included at max growth)
        self.apex_offset = max(1.0, 0.5 * (self.max_z - self.min_z))

    def update(self, dt):
        # compute phase t and smooth 0→1→0 scale using a sine wave
        t = (self.time_elapsed * (2 * np.pi / self.cycle_time)) % (2 * np.pi)
        smooth = (np.sin(t - np.pi / 2) + 1) / 2.0  # 0..1

        # map smooth value to growth factor in [growth_min, growth_max]
        growth = self.growth_min + smooth * (self.growth_max - self.growth_min)

        # pick a new color when the wave is at its minimum (start of expansion)
        if np.sin(t - np.pi / 2) < -0.999:
            self.color = np.array(self.cm.next_color(), dtype=float)

        # vertical normalization using Animation's bounds, with a small apex offset
        z_vals = np.array([p[2] for p in self.coords])
        z_min, z_max = self.min_z, self.max_z
        # allow tip of cone to be above the highest LED so the top LEDs can be inside the cone
        apex_offset = getattr(self, 'apex_offset', None)
        if apex_offset is None:
            apex_offset = max(1.0, 0.02 * (z_max - z_min if z_max != z_min else 1.0))
            self.apex_offset = apex_offset
        z_eff_max = z_max + apex_offset
        z_range = z_eff_max - z_min if z_eff_max != z_min else 1.0
        z_norm = np.clip((z_vals - z_min) / z_range, 0.0, 1.0)  # 0..1 (0 at bottom, 1 at effective top)

        # radial distances and cone profile using Animation.radius
        x_vals = np.array([p[0] for p in self.coords])
        y_vals = np.array([p[1] for p in self.coords])
        radii = np.sqrt(x_vals ** 2 + y_vals ** 2)

        # cone radius at each height: (1 - z_norm) * self.radius * growth
        radius_profile = (1.0 - z_norm) * float(self.radius) * growth

        # inside cone mask
        inside_mask = radii <= radius_profile

        # fade near the cone boundary
        boundary_scale = max(self.boundary_fraction * max(1.0, float(self.radius)), 1e-6)
        boundary_dist = np.clip((radius_profile - radii) / boundary_scale, 0.0, 1.0)

        brightness = inside_mask.astype(float) * boundary_dist

        # apply color and clamp
        colors = self.color[None, :] * brightness[:, None]
        colors = np.clip(colors, 0, 255).astype(np.uint8)

        for i in range(self.num_pixels):
            self.pixels[i] = tuple(colors[i])