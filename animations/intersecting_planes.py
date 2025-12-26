import random
import time

# Tree boundaries for bouncing (from your scanned coordinates)
TREE_X_MIN, TREE_X_MAX = -25, 25
TREE_Y_MIN, TREE_Y_MAX = -25, 25
TREE_Z_MIN, TREE_Z_MAX = -50, 50   # z is height

# Plane settings
NUM_PLANES = 3
PLANE_SIZE = 100  # Approximate size of the plane
SPEED = 1        # Movement speed per frame

# Time per frame
FRAME_DELAY = 0.05

# -----------------------------
# PLANE CLASS
# -----------------------------
class Plane:
    def __init__(self):
        self.x = random.uniform(TREE_X_MIN, TREE_X_MAX)
        self.y = random.uniform(TREE_Y_MIN, TREE_Y_MAX)
        self.z = random.uniform(TREE_Z_MIN, TREE_Z_MAX)
        self.dx = random.uniform(-SPEED, SPEED)
        self.dy = random.uniform(-SPEED, SPEED)
        self.dz = random.uniform(-SPEED, SPEED)
        self.color = [random.randint(0, 255) for _ in range(3)]
    
    def move(self):
        # Update position
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

        # Bounce off tree boundaries
        if self.x < TREE_X_MIN or self.x > TREE_X_MAX:
            self.dx *= -1
        if self.y < TREE_Y_MIN or self.y > TREE_Y_MAX:
            self.dy *= -1
        if self.z < TREE_Z_MIN or self.z > TREE_Z_MAX:
            self.dz *= -1

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def average_color(c1, c2):
    return [(a+b)//2 for a,b in zip(c1,c2)]

# -----------------------------
# INITIALIZE PLANES
# -----------------------------
planes = [Plane() for _ in range(NUM_PLANES)]

# -----------------------------
# MAIN LOOP
# -----------------------------
def run(coords, pixels, duration = None):
    start_time = time.time()

    while duration is None or time.time() - start_time < duration:
        # Clear pixels
        pixels.fill((0, 0, 0))

        # Move planes
        for plane in planes:
            plane.move()

        # Update LEDs
        for i, coord in enumerate(coords):
            led_color = [0, 0, 0]
            for plane in planes:
                # Check if LED is within plane's influence
                if (abs(coord[0] - plane.x) < PLANE_SIZE and
                    abs(coord[1] - plane.y) < PLANE_SIZE and
                    abs(coord[2] - plane.z) < PLANE_SIZE):
                    led_color = average_color(led_color, plane.color)
            pixels[i] = tuple(led_color)

        pixels.show()
        time.sleep(FRAME_DELAY)