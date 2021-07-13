from __future__ import annotations

from typing import Tuple

import game.game_map


class Entity:
    """A generic object to represent players, enemies, items, etc."""

    def __init__(
        self,
        gamemap: game.game_map.GameMap,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
    ):
        self.gamemap = gamemap
        gamemap.entities.add(self)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
