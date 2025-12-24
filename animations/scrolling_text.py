import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import my_utils

TEXT = "MERRYCHRISTMAS!"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 80

IMG_WIDTH = 200
IMG_HEIGHT = 100
FPS = 60

ROTATE_SPEED = -0.05         # negative = rotate right→left
FACE_WIDTH = 2 * np.pi            # angular width of visible face
EDGE_FADE = 0.1             # fade near edges
PAUSE_BETWEEN_LETTERS = 0.0  # seconds to hold between rotations

LETTER_COLORS = np.array([
    [255,  0,  0],   # red
    [ 0, 255,  0],   # green
    [ 0,  0, 255],   # blue
    [255, 255,  0],   # yellow
    [255,  0, 255],   # magenta
    [ 0, 255, 255],   # cyan
    [255, 255, 255],   # white
], dtype=float)

BG_COLOR = np.array([0, 0, 0], dtype=float)

# ===================================================
# PREPARE LETTER IMAGES
# ===================================================
def make_letter_image(letter: str):
    img = Image.new("L", (IMG_WIDTH, IMG_HEIGHT), 0)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    w, h = draw.textsize(letter, font=font)
    draw.text(((IMG_WIDTH - w) / 2, (IMG_HEIGHT - h) / 2), letter, fill=255, font=font)
    return np.array(img) / 255.0

# ===================================================
# MAIN LOOP
# ===================================================
def run(coords, pixels, duration):
    start_time = time.time()
    NUM_LEDS = len(coords)

    coords -= np.mean(coords, axis=0)

    frame_delay = 1.0 / FPS
    angle = 0.0
    letter_index = 0

    letters = [make_letter_image(ch) for ch in TEXT]

    # ===================================================
    # NORMALIZE GEOMETRY
    # ===================================================
    z_vals = coords[:, 2]
    z_min, z_max = np.min(z_vals), np.max(z_vals)
    z_norm = (z_vals - z_min) / (z_max - z_min)
    radius = np.max(np.linalg.norm(coords[:, :2], axis=1))
    angles = np.arctan2(coords[:, 1], coords[:, 0])  # radians around Z
    angles = (angles + np.pi) % (2 * np.pi)


    while time.time() - start_time < duration:
        img = letters[letter_index]
        color = LETTER_COLORS[letter_index % len(LETTER_COLORS)]

        pixels_buf = np.zeros((NUM_LEDS, 3), dtype=float)

        # Render one letter only
        delta = (angles - angle + np.pi) % (2 * np.pi) - np.pi
        mask = np.abs(delta) < FACE_WIDTH / 2

        # 2D mapping for projection
        u = (delta / (FACE_WIDTH / 2)) * 0.5 + 0.5  # horizontal coordinate
        v = z_norm                                 # vertical coordinate

        x_idx = np.clip((u * (IMG_WIDTH - 1)).astype(int), 0, IMG_WIDTH - 1)
        y_idx = np.clip(((1 - v) * (IMG_HEIGHT - 1)).astype(int), 0, IMG_HEIGHT - 1)

        brightness = np.zeros_like(u)
        brightness[mask] = img[y_idx[mask], x_idx[mask]]

        # soft fade near slice edges
        if EDGE_FADE > 0:
            edge_fade = 1 - np.clip((np.abs(delta) - (FACE_WIDTH/2 - EDGE_FADE)) / EDGE_FADE, 0, 1)
            brightness *= edge_fade

        pixels_buf += (color - BG_COLOR) * brightness[:, None]

        # Display
        pixels_buf = np.clip(pixels_buf, 0, 255).astype(np.uint8)
        for i in range(NUM_LEDS):
            pixels[i] = tuple(pixels_buf[i])
        pixels.show()

        # advance rotation
        angle += ROTATE_SPEED

        # when one full rotation finishes, move to next letter
        if abs(angle) >= 2 * np.pi:
            angle = 0.0
            letter_index = (letter_index + 1) % len(letters)
            time.sleep(PAUSE_BETWEEN_LETTERS)

        time.sleep(frame_delay)