from __future__ import annotations

from typing import NamedTuple, Tuple, Type, TYPE_CHECKING

import ai
from actor import Actor

if TYPE_CHECKING:
    from game_map import GameMap


class Race(NamedTuple):
    name: str
    char: str
    color: Tuple[int, int, int]

    max_hp: int
    defense: int
    power: int

    blocks_movement: bool = True
    ai_cls: Type[ai.AI] = ai.AI

    def spawn(self, gamemap: GameMap, x: int, y: int) -> Actor:
        """Spawn a copy of this instance at the given location."""
        entity = Actor(gamemap, x, y, race=self)
        gamemap.entities.add(entity)
        return entity
