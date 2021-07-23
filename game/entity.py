from __future__ import annotations

from typing import Optional, Tuple, Type, Union

import game.components.ai
import game.components.consumable
import game.components.fighter
import game.components.inventory
import game.game_map
import game.render_order


class Entity:
    """A generic object to represent players, enemies, items, etc."""

    def __init__(
        self,
        parent: Union[game.game_map.GameMap, game.components.inventory.Inventory],
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: game.render_order.RenderOrder = game.render_order.RenderOrder.CORPSE,
    ):
        self.parent = parent
        if isinstance(parent, game.game_map.GameMap):
            parent.entities.add(self)

        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

    @property
    def gamemap(self) -> game.game_map.GameMap:
        return self.parent.gamemap


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
        inventory: Optional[game.components.inventory.Inventory] = None,
    ):
        super().__init__(
            gamemap,
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

        if inventory is None:
            inventory = game.components.inventory.Inventory(0)
        self.inventory = inventory
        self.inventory.entity = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


class Item(Entity):
    def __init__(
        self,
        parent: Union[game.game_map.GameMap, game.components.inventory.Inventory],
        x: int = 0,
        y: int = 0,
        *,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: game.components.consumable.Consumable,
    ):
        super().__init__(
            parent,
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=game.render_order.RenderOrder.ITEM,
        )
        if isinstance(parent, game.components.inventory.Inventory):
            parent.items.append(self)

        self.consumable = consumable
        self.consumable.parent = self
