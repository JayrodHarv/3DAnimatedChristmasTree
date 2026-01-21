class AnimationController:
    def __init__(self, animations):
        self.animations = animations
        self.index = 0
        self.speed = 1.0
        self.paused = False

    def current(self):
        return self.animations[self.index]

    def play(self, name):
        for i, anim in enumerate(self.animations):
            if anim.name == name:
                self.index = i
                return
        raise KeyError(name)

    def next(self):
        self.index = (self.index + 1) % len(self.animations)

    def previous(self):
        self.index = (self.index - 1) % len(self.animations)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def toggle(self):
        self.paused = not self.paused

    def set_speed(self, value):
        self.speed = max(0.05, value)

    def list_animations(self):
        return [a.name for a in self.animations]

    def status(self):
        return {
            "current": self.current().name,
            "paused": self.paused,
            "speed": self.speed,
        }

