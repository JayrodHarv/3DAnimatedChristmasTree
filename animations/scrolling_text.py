import numpy as np
from PIL import Image, ImageDraw, ImageFont
from animations.animation import Animation

TEXT = "MERRYCHRISTMAS!"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 80

IMG_WIDTH = 200
IMG_HEIGHT = 100

ROTATE_SPEED = -0.5         # negative = rotate right→left
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

class ScrollingTextAnimation(Animation):
    name = "Scrolling Text"

    def setup(self):
        self.NUM_LEDS = self.num_pixels

        self.coords -= np.mean(self.coords, axis=0)

        # rotation speed in radians per second — preserve previous per-frame behavior
        # previous code used ROTATE_SPEED per frame at FPS frames/sec, so scale to per-second
        self.rotation_speed = ROTATE_SPEED
        # pause timer (seconds) between letters
        self.pause_remaining = 0.0

        self.angle = 0.0
        self.letter_index = 0

        self.letters = [make_letter_image(ch) for ch in TEXT]

        # NORMALIZE GEOMETRY
        z_vals = self.coords[:, 2]
        z_min, z_max = np.min(z_vals), np.max(z_vals)
        self.z_norm = (z_vals - z_min) / (z_max - z_min)
        self.radius = np.max(np.linalg.norm(self.coords[:, :2], axis=1))
        self.angles = np.arctan2(self.coords[:, 1], self.coords[:, 0])  # radians around Z
        self.angles = (self.angles + np.pi) % (2 * np.pi)

    def update(self, dt):
        img = self.letters[self.letter_index]
        color = LETTER_COLORS[self.letter_index % len(LETTER_COLORS)]

        pixels_buf = np.zeros((self.NUM_LEDS, 3), dtype=float)

        # Render one letter only
        delta = (self.angles - self.angle + np.pi) % (2 * np.pi) - np.pi
        mask = np.abs(delta) < FACE_WIDTH / 2

        # 2D mapping for projection
        u = (delta / (FACE_WIDTH / 2)) * 0.5 + 0.5  # horizontal coordinate
        v = self.z_norm                                 # vertical coordinate

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
        for i in range(self.NUM_LEDS):
            self.pixels[i] = tuple(pixels_buf[i])
        # handle pause between letters using dt
        if self.pause_remaining > 0.0:
            self.pause_remaining = max(0.0, self.pause_remaining - dt)
        else:
            # advance rotation using per-second rotation speed
            self.angle += self.rotation_speed * dt

            # when one full rotation finishes, move to next letter and start pause
            if abs(self.angle) >= 2 * np.pi:
                self.angle = 0.0
                self.letter_index = (self.letter_index + 1) % len(self.letters)
                self.pause_remaining = PAUSE_BETWEEN_LETTERS