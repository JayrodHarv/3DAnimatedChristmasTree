from animations import ANIMATIONS

class AnimationController:
    def __init__(self, animations):
        self.animations = animations
        self.index = 0
        self.speed = 1.0
        self.paused = False

    def current(self):
        return self.animations[self.index]

    def next(self):
        self.index = (self.index + 1) % len(self.animations)

    def previous(self):
        self.index = (self.index - 1) % len(self.animations)

    def play(self, name):
        for i, anim in enumerate(self.animations):
            if anim.name == name:
                self.index = i
                return
        raise KeyError(f"Unknown animation: {name}")

    def set_speed(self, value):
        self.speed = max(0.05, value)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def status(self):
        return {
            "current": self.current().name,
            "paused": self.paused,
            "speed": self.speed,
        }

controller = AnimationController(ANIMATIONS)