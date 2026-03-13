class Renderer:

    def __init__(self, pixels):
        self.pixels = pixels

    def set_pixel(self, i, color):
        self.pixels[i] = color

    def clear(self):
        for i in range(len(self.pixels)):
            self.pixels[i] = (0,0,0)

    def show(self):
        self.pixels.show()