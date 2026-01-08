import math
from utils import color_manager
from animations.animation import Animation

class RGBSpheresAnimation(Animation):
    name = "RGB Spheres"

    def setup(self):
        # center height for spawning spheres
        self.center_z = self.max_z / 2.0

        # distances measured from the tree center so culling and max radius are correct
        self.distances = [
            math.sqrt(x*x + y*y + (z - self.center_z)**2)
            for x, y, z in self.coords
        ]
        self.max_radius = max(self.distances)

        self.expansion_speed = self.max_radius / 6.0   # units per second
        self.spawn_interval = 3                 # seconds

        self.spheres = []
        self.last_spawn = 0
        self.time_accumulator = 0
        self.frame_delay = 0.03

        self.color_manager = color_manager.ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

    def update(self, dt):
        self.time_accumulator += dt

        # Spawn new sphere at center height of the tree
        if self.time_accumulator - self.last_spawn >= self.spawn_interval:
            self.spheres.append({
                "radius": 0.0,
                "color": self.color_manager.next_color(),
                # spawn vertically at middle of tree
                "center_z": self.max_z / 2.0
            })
            self.last_spawn = self.time_accumulator

        # Grow spheres using elapsed time
        for s in self.spheres:
            s["radius"] += self.expansion_speed * dt

        # Cull old spheres
        self.spheres = [
            s for s in self.spheres
            if s["radius"] <= self.max_radius * 1.2
        ]

        # Update pixels — compute distance from each pixel to the sphere center
        for j, (x, y, z) in enumerate(self.coords):
            pixel_color = None

            # iterate newest spheres first
            for s in reversed(self.spheres):
                dist = math.sqrt(x*x + y*y + (z - s["center_z"])**2)
                if dist <= s["radius"]:
                    pixel_color = s["color"]
                    break

            if pixel_color:
                self.pixels[j] = pixel_color