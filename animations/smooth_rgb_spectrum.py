import time
import colorsys

def run(coords, pixels, duration = None):
    start_time = time.time()
    fps = 30
    hue_speed = 0.02   # smaller = slower transition

    hue = 0.0

    while True:
        # Exit condition
        if duration is not None and time.time() - start_time >= duration:
            break

        # Convert hue -> RGB
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))

        pixels.fill(color)
        pixels.show()

        hue = (hue + hue_speed / fps) % 1.0
        time.sleep(1 / fps)