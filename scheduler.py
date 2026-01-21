import time

def run_scheduler(pixels, coords, controller, fps=60):
    last = time.time()

    while True:
        now = time.time()
        dt = now - last
        last = now

        if not controller.paused:
            anim = controller.current()
            anim.update(dt * controller.speed)
            pixels.show()

        time.sleep(1 / fps)