import time

class Animation:
    name = "Unnamed"

    def __init__(self, coords, pixels):
        # Light stuff
        self.coords = coords
        self.pixels = pixels
        self.num_pixels = len(pixels)

        # Timing stuff
        self.time_elapsed = 0

        # ---- Tree bounds (computed once) ----
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        zs = [p[2] for p in coords]

        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)
        self.min_z, self.max_z = min(zs), max(zs)
        
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

    def run(self, duration=None, fps=30, speed=1.0):
        self.setup()
        start = last = time.time()

        prev_remaining = None
        while duration is None or time.time() - start < duration:
            now = time.time()
            dt = now - last
            last = now

            scaled_dt = dt * speed

            self.time_elapsed += scaled_dt

            self.update(scaled_dt)
            self.draw()

            # If a finite duration was provided, print a single-line countdown
            if duration is not None:
                elapsed = time.time() - start
                remaining = max(0, int(duration - elapsed))
                if remaining != prev_remaining:
                    try:
                        print(f"\rPlaying {self.name}: {remaining}s remaining", end="", flush=True)
                    except Exception:
                        # If stdout is not available or writing fails, ignore
                        pass
                    prev_remaining = remaining

            time.sleep(max(0, 1 / fps))

        # If we printed a countdown, finish the line so further prints don't overwrite it
        if duration is not None:
            try:
                print()
            except Exception:
                pass
