import math
from utils import color_manager
from animations.animation import Animation

class TreeCeptionAnimation(Animation):
    name = "Tree-ception"

    def setup(self):
        # precompute per-pixel radial distances and z values for cone rendering
        self.radial = [math.sqrt(x*x + y*y) for x, y, z in self.coords]
        self.z_vals = [z for _, _, z in self.coords]
        # allow extra padding so cones can grow beyond the measured tree radius
        # (increase factor to ensure fully-grown cones can reach every LED)
        self.max_radius = max(self.radial) * 2 + 10

        # small apex offset so the cone tip sits slightly above the highest LED
        # (helps ensure top LEDs can be included when the cone is fully grown)
        self.apex_offset = max(1.0, 0.5 * (self.max_z - self.min_z))

        # cone growth speed (g units per second, where g goes 0→1)
        self.growth_speed = 0.5
        self.spawn_interval = 2.5  # seconds between cones

        self.cones = []  # each: {"g": float, "color": (r,g,b)}
        # start last_spawn negative so the first cone spawns immediately
        self.last_spawn = -self.spawn_interval
        self.frame_delay = 0.03

        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

    def update(self, dt):
        # Spawn new cone (growth scalar g starts at 0)
        if self.time_elapsed - self.last_spawn >= self.spawn_interval:
            self.cones.append({
                "g": 0.0,
                "color": self.color_manager.next_color()
            })
            self.last_spawn = self.time_elapsed

        # Grow cones using elapsed time
        for c in self.cones:
            c["g"] += self.growth_speed * dt

        # Cull old cones (allow a little overshoot past g=1 so cones can extend beyond measured radius)
        self.cones = [c for c in self.cones if c["g"] <= 1.5]

        # Update pixels — render cones using vertical profile
        for j, z in enumerate(self.z_vals):
            pixel_color = None

            # fraction up the tree with a small apex offset so top LEDs aren't at an exact zero-radius tip
            z_eff_max = self.max_z + getattr(self, 'apex_offset', 0.0)
            z_range = z_eff_max - self.min_z if z_eff_max != self.min_z else 1.0
            frac_height = (z - self.min_z) / z_range
            frac_height = max(0.0, min(1.0, frac_height))

            # cone radius at this height when fully grown
            full_r = self.max_radius * (1.0 - frac_height)

            # iterate newest cones first (newest wins)
            for c in reversed(self.cones):
                if self.radial[j] <= full_r * c["g"]:
                    pixel_color = c["color"]
                    break

            if pixel_color:
                self.pixels[j] = pixel_color