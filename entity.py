from __future__ import annotations

import copy
from typing import List, Tuple, Type, TypeVar, TYPE_CHECKING

import tcod.path

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from game_map import GameMap


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

    def spawn(self, gamemap: GameMap, x: int, y: int) -> Entity:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone

    def get_first_step_towards_destination(self, target_x: int, target_y: int, game_map: GameMap) -> Tuple[int, int]:
        return self.get_path_astar(target_x, target_y, game_map)[0]

    def get_path_astar(self, target_x: int, target_y: int, game_map: GameMap) -> List[Tuple[int, int]]:
        astar = tcod.path.AStar(game_map.tiles["walkable"])

        return astar.get_path(self.x, self.y, target_x, target_y)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai: BaseAI,
        fighter: Fighter,
        inventory: Inventory
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR
        )

        self.ai = ai
        self.ai.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self


class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Consumable
    ):
        super().__init__(x=x, y=y, char=char, color=color, name=name, blocks_movement=False,
                         render_order=RenderOrder.ITEM)

        self.consumable = consumable
        self.consumable.parent = self


def register(cls: Type[Entity]) -> None:
    assert issubclass(cls, Entity)


register(Entity)
register(Actor)
register(Item)
