import numpy as np  # type: ignore
from tcod.console import Console

graphic_dt = np.dtype([("ch", np.int32), ("fg", "3B"), ("bg", "3B")])

tile_dt = np.dtype(
    [("walkable", np.bool), ("transparent", np.bool), ("dark", graphic_dt)]
)

floor = np.array((True, True, (ord(" "), 255, (50, 50, 150))), dtype=tile_dt)
wall = np.array((False, False, (ord(" "), 255, (0, 0, 100))), dtype=tile_dt)


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=floor, order="F")

        self.tiles[30:33, 22] = wall

    def render(self, console: Console):
        console.tiles_rgb[0 : self.width, 0 : self.height] = self.tiles["dark"]
