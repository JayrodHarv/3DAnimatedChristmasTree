class Animation:

    def __init__(self, tree, renderer, color_manager):
        self.tree = tree
        self.coords = tree.coords
        self.renderer = renderer
        self.color_manager = color_manager
        self.t = 0

    def update(self, dt):
        self.t += dt