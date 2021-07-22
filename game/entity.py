from __future__ import annotations

from typing import Optional, Tuple, Type

import game.components.ai
import game.components.fighter
import game.game_map
import game.render_order


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
        render_order: game.render_order.RenderOrder = game.render_order.RenderOrder.CORPSE,
    ):
        self.gamemap = gamemap
        gamemap.entities.add(self)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order


class Actor(Entity):
    def __init__(
        self,
        gamemap: game.game_map.GameMap,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        *,
        ai_cls: Type[game.components.ai.BaseAI],
        fighter: game.components.fighter.Fighter,
    ):
        super().__init__(
            gamemap=gamemap,
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=game.render_order.RenderOrder.ACTOR,
        )

        self.ai: Optional[game.components.ai.BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
