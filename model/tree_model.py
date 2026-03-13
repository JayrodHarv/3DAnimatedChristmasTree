class TreeModel:

    def __init__(self, coords):

        self.coords = coords
        self.num_pixels = len(coords)

        xs = [x for x,_,_ in coords]
        ys = [y for _,y,_ in coords]
        zs = [z for _,_,z in coords]

        self.min_x = min(xs)
        self.max_x = max(xs)

        self.min_y = min(ys)
        self.max_y = max(ys)

        self.min_z = min(zs)
        self.max_z = max(zs)

        self.height = self.max_z - self.min_z
        self.radius = max((x**2 + y**2)**0.5 for x,y,_ in coords)

        self.center_z = (self.min_z + self.max_z) / 2