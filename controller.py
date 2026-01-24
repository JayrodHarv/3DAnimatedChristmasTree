from animations import create_animations
from utils import runtime
import time
import random
import subprocess

class AnimationController:
    def __init__(self, animations):
        self.animations = animations
        self.order = list(range(len(animations)))
        self.index = 0
        self.speed = 1.0
        self.paused = False

        self.until_time = None
        self.shuffle_mode = True # start in shuffle mode
        self.shuffle_duration = 30  # default seconds per animation

    def current(self):
        return self.animations[self.index]
    
    def start_shuffle(self, duration):
        self.shuffle_mode = True
        self.shuffle_duration = duration
        
        self.order = list(range(len(self.animations)))
        random.shuffle(self.order)

        self.index = 0
        self._start_current_timer()

        self.current().reset()
        self.current().clear()

    def stop_shuffle(self):
        self.shuffle_mode = False
        self.until_time = None

    def _start_current_timer(self):
        self.until_time = time.time() + self.shuffle_duration

    def next(self):
        self.current().reset() # reset current animation
        self.current().clear() # clear current animation
        self.index = (self.index + 1) % len(self.animations)

        if self.shuffle_mode:
            self._start_current_timer()
        else:
            self.until_time = None

    def previous(self):
        self.animations[self.index].reset() # reset current animation
        self.animations[self.index].clear() # clear current animation
        self.index = (self.index - 1) % len(self.animations)

    def play(self, name):
        self.shuffle_mode = False # stop shuffle mode if manual play
        self.animations[self.index].reset() # reset current animation
        self.animations[self.index].clear() # clear current animation
        for i, anim in enumerate(self.animations):
            if anim.name == name:
                self.index = i
                return
        raise KeyError(f"Unknown animation: {name}")

    def set_speed(self, value):
        self.speed = max(0.05, value)

    def toggle(self):
        self.paused = not self.paused

    def status(self):
        return {
            "current": self.current().name,
            "paused": self.paused,
            "speed": self.speed,
            "mode": "shuffle" if self.shuffle_mode else "normal",
            "until": self.until_time,
        }
    
    def list_animations(self):
        return [anim.name for anim in self.animations]
    
    def update_timer(self):
        if self.until_time is not None and time.time() >= self.until_time:
            self.next()

    def safe_shutdown(self, pixels):
        try:
            pixels.fill((0, 0, 0)) # turn off all pixels
            pixels.show()
            time.sleep(0.5)
        except Exception:
            pass
        # Now issue shutdown command
        subprocess.Popen(["sudo", "/sbin/shutdown", "-h", "now"])
    
COORDS_FILE = "tree_d_coords.txt"

# Load hardware + data
coords, pixels = runtime.setup_tree(
    coords_file=COORDS_FILE
)
    
animations = create_animations(coords, pixels)

controller = AnimationController(animations)