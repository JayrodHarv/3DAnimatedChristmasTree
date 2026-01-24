from animations import create_animations
from utils import runtime

class AnimationController:
    def __init__(self, animations):
        self.animations = animations
        self.index = 0
        self.speed = 1.0
        self.paused = False

    def current(self):
        return self.animations[self.index]

    def next(self):
        self.animations[self.index].reset() # reset current animation
        self.animations[self.index].clear() # clear current animation
        self.index = (self.index + 1) % len(self.animations)

    def previous(self):
        self.animations[self.index].reset() # reset current animation
        self.animations[self.index].clear() # clear current animation
        self.index = (self.index - 1) % len(self.animations)

    def play(self, name):
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
        }
    
    def list_animations(self):
        return [anim.name for anim in self.animations]
    
COORDS_FILE = "tree_d_coords.txt"

# Load hardware + data
coords, pixels = runtime.setup_tree(
    coords_file=COORDS_FILE
)
    
animations = create_animations(coords, pixels)

controller = AnimationController(animations)