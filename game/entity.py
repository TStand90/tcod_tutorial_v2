from __future__ import annotations

from typing import Tuple, TypeVar

import game.game_map

T = TypeVar("T", bound="Entity")


class Entity:
    """A generic object to represent players, enemies, items, etc."""

    def __init__(
        self,
        gamemap: game.game_map.GameMap,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        name: str,
        blocks_movement: bool = True,
    ):
        self.gamemap = gamemap
        gamemap.entities.add(self)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
