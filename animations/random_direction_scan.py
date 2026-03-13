from utils import my_utils
from .animation import Animation

class RandomDirectionScanAnimation(Animation):

    name = "Random Direction Scan"

    def __init__(self, tree, renderer, color_manager):
        super().__init__(tree, renderer, color_manager)
        self.reset()

    def reset(self):
        self.rotated_coords = my_utils.randomly_rotate_tree(self.coords)

        self.turn_on_min = 0
        self.turn_on_max = self.tree.max_z / 10

        self.current_color = self.color_manager.next_color()

    def update(self, dt):
        super().update(dt)

        speed = (self.tree.max_z / 2) * dt

        self.turn_on_min += speed
        self.turn_on_max += speed

        if self.turn_on_min > self.tree.max_z:

            self.turn_on_min = 0
            self.turn_on_max = self.tree.max_z / 10

            self.current_color = self.color_manager.next_color()

            self.rotated_coords = my_utils.randomly_rotate_tree(self.coords)

        for i, (_, _, z) in enumerate(self.rotated_coords):

            if self.turn_on_min <= z <= self.turn_on_max:
                self.renderer.set_pixel(i, self.current_color)
            else:
                self.renderer.set_pixel(i, (0, 0, 0))