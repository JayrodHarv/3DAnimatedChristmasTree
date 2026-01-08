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
        self.max_radius = max(self.radial) * 1.75 + 10

        # cone growth speed (g units per second, where g goes 0→1)
        self.growth_speed = 0.5
        self.spawn_interval = 2.5  # seconds between cones

        self.cones = []  # each: {"g": float, "color": (r,g,b)}
        self.last_spawn = 0
        self.time_accumulator = 0
        self.frame_delay = 0.03

        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

    def update(self, dt):
        self.time_accumulator += dt

        # Spawn new cone (growth scalar g starts at 0)
        if self.time_accumulator - self.last_spawn >= self.spawn_interval:
            self.cones.append({
                "g": 0.0,
                "color": self.color_manager.next_color()
            })
            self.last_spawn = self.time_accumulator

        # Grow cones using elapsed time
        for c in self.cones:
            c["g"] += self.growth_speed * dt

        # Cull old cones
        self.cones = [c for c in self.cones if c["g"] <= 1.2]

        # Update pixels — render cones using vertical profile
        for j, z in enumerate(self.z_vals):
            pixel_color = None

            # fraction up the tree (0 at bottom -> 1 at top)
            frac_height = z / self.max_z
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