from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item


class Inventory(BaseComponent):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def add_item(self, item: Item) -> bool:
        """
        Adds an item to the inventory, if there is room for it.
        If the item was added, return True to represent a turn passing. If not, return False, so the player does not
        waste a turn.
        """
        if len(self.items) >= self.capacity:
            return False
        else:
            self.items.append(item)

            return True

    def drop(self, item: Item, engine: Engine):
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)

        engine.game_map.entities.add(item)

        item.x, item.y = self.parent.x, self.parent.y

        engine.message_log.add_message(f"You dropped the {item.name}.")
