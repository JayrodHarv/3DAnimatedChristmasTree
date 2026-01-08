import time

class Animation:
    name = "Unnamed"

    def __init__(self, coords, pixels):
        self.coords = coords
        self.pixels = pixels
        self.num_pixels = len(pixels)

        # ---- Tree bounds (computed once) ----
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        zs = [p[2] for p in coords]

        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)
        self.min_z, self.max_z = min(zs), max(zs)

        self.height = self.max_z - self.min_z
        self.radius = max(
            max(abs(self.min_x), abs(self.max_x)),
            max(abs(self.min_y), abs(self.max_y))
        )

    def setup(self):
        pass

    def update(self, dt):
        raise NotImplementedError

    def draw(self):
        self.pixels.show()

    def run(self, duration=None, fps=30):
        self.setup()
        start = last = time.time()

        while duration is None or time.time() - start < duration:
            now = time.time()
            dt = now - last
            last = now

            self.update(dt)
            self.draw()

            time.sleep(max(0, 1 / fps))
