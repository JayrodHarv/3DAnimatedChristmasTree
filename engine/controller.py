import random
import time
from animations import ANIMATIONS
from utils.color_manager import ColorManager

class AnimationController:

    def __init__(self, tree, renderer):
        self.tree = tree
        self.renderer = renderer

        self.color_manager = ColorManager()
        self.color_manager.generate_pleasant_colors()
        self.color_manager.shuffle()

        # Initialize animations
        self.animations = [
            a(tree, renderer, self.color_manager) for a in ANIMATIONS
        ]

        # Start with the first animation
        self.index = 0
        self.current = self.animations[0]

        self.last = time.time()

    def update(self):
        now = time.time()
        dt = now - self.last
        self.last = now

        self.current.update(dt)
        self.renderer.show()

    def next(self):
        self.index = (self.index + 1) % len(self.animations)
        self.current = self.animations[self.index]

    def previous(self):
        self.index = (self.index - 1) % len(self.animations)
        self.current = self.animations[self.index]

    def shuffle(self):
        self.current = random.choice(self.animations)

    def set(self,name):
        for a in self.animations:
            if a.__class__.__name__ == name:
                self.current = a