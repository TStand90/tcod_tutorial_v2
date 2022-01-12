from __future__ import annotations

from typing import List

import game.entity
from game.components.base_component import BaseComponent


class Inventory(BaseComponent):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[game.entity.Item] = []

    def drop(self, item: game.entity.Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)

        item.parent = self.gamemap
        self.gamemap.entities.add(item)
        item.x = self.parent.x
        item.y = self.parent.y

        self.engine.message_log.add_message(f"You dropped the {item.name}.")
