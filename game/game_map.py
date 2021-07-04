from __future__ import annotations

from typing import Set

import numpy as np

import game.engine
import game.entity


class GameMap:
    def __init__(self, engine: game.engine.Engine, width: int, height: int):
        self.engine = engine
        self.width, self.height = width, height
        self.tiles = np.zeros((width, height), dtype=bool, order="F")
        self.entities: Set[game.entity.Entity] = set()

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
