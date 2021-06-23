import numpy as np
import tcod

import game.tiles


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=game.tiles.wall, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: tcod.Console) -> None:
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["dark"]
