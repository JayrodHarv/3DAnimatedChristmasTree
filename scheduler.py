import time

def run_scheduler(pixels, coords, controller, fps=60):
    last = time.time()

    while True:
        now = time.time()
        dt = now - last
        last = now

        if not controller.paused:
            AnimClass = controller.current()
            anim = AnimClass(coords, pixels)
            anim.update(dt * controller.speed)
            pixels.show()

        time.sleep(1 / fps)