import colorsys
import random
from typing import List, Tuple

RGB = Tuple[int, int, int]

class ColorManager:
    def __init__(self):
        self.colors: List[RGB] = []
        self._index: int = 0
    
    def generate_pleasant_colors(self, count: int = 12, saturation: float = 1, value: float = 1) -> List[RGB]:

        self.colors.clear()

        for i in range(count):
            h = i / count
            r, g, b = colorsys.hsv_to_rgb(h, saturation, value)
            self.colors.append((
                int(r * 255),
                int(g * 255),
                int(b * 255)
            ))

        return self.colors
    
    def shuffle(self) -> None:
        random.shuffle(self.colors)
        self._index = 0

    def get_colors(self) -> List[RGB]:
        return self.colors.copy()
    
    def next_color(self) -> RGB:
        if not self.colors:
            raise ValueError("Colors not yet generated.")
        
        color = self.colors[self._index]
        self._index = (self._index + 1) % len(self.colors)

        return color