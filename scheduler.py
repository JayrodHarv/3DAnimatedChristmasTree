import time

def run_scheduler(pixels, coords, controller, fps=30):
    last = time.time()

    while True:
        now = time.time()
        dt = now - last
        last = now

        if not controller.paused:
            AnimClass = controller.current()
            anim = AnimClass(coords, pixels)
            anim.setup()

            scaled_dt = dt * controller.speed
            anim.update(scaled_dt)

            anim.time_elapsed += scaled_dt

            pixels.show()

        time.sleep(max(0, 1 / fps))