from __future__ import annotations

from typing import TYPE_CHECKING

from entity import Entity

if TYPE_CHECKING:
    from game_map import GameMap
    from race import Race


class Actor(Entity):
    def __init__(self, gamemap: GameMap, x: int, y: int, race: Race) -> None:
        super().__init__(
            gamemap=gamemap,
            x=x,
            y=y,
            char=race.char,
            color=race.color,
            name=race.name,
            blocks_movement=race.blocks_movement,
        )
        self.race = race
        self.hp = race.max_hp
        self.ai = race.ai_cls(self)
