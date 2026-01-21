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
            anim.update(dt * controller.speed)
            pixels.show()

        time.sleep(max(0, 1 / fps))