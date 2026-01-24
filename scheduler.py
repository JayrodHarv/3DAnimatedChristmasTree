import time

_stop = False

def stop_scheduler():
    global _stop
    _stop = True

def run_scheduler(pixels, coords, controller, fps=30):
    global _stop

    last = time.time()
    max_dt = 1.0 / fps * 2  # safety clamp

    while not _stop:
        now = time.time()
        dt = now - last
        last = now

        dt = min(dt, max_dt)

        if not controller.paused:
            anim = controller.current()

            scaled_dt = dt * controller.speed
            anim.time_elapsed += scaled_dt

            anim.update(scaled_dt)

            pixels.show()

        time.sleep(max(0, 1 / fps))