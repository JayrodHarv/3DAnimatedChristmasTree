import time

def run_scheduler(pixels, coords, controller, fps=30):
    last = time.time()
    max_dt = 1.0 / fps * 2  # safety clamp

    while True:
        now = time.time()
        dt = now - last
        last = now

        dt = min(dt, max_dt)

        if not controller.paused:
            AnimClass = controller.current()
            anim = AnimClass(coords, pixels)
            anim.setup()

            scaled_dt = dt * controller.speed
            anim.time_elapsed += scaled_dt

            anim.update(scaled_dt)

            pixels.show()

        time.sleep(max(0, 1 / fps))