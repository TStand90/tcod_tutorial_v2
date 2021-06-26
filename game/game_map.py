from __future__ import annotations

from typing import Iterable

from tcod.console import Console
import numpy as np

import game.engine
import game.tiles


class GameMap:
    def __init__(
        self, engine: game.engine.Engine, width: int, height: int, entities: Iterable[game.entity.Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=game.tiles.floor, order="F")

        self.tiles[30:33, 22] = game.tiles.wall

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["dark"]

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
