from __future__ import annotations

import logging

import game.entity

logger = logging.getLogger(__name__)


class Action:
    def __init__(self, entity: game.entity.Entity) -> None:
        super().__init__()
        self.entity = entity  # The object performing the action.
        self.engine = entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action now.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: game.entity.Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        raise NotImplementedError()


class Melee(ActionWithDirection):
    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy
        target = self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack.

        logger.info(f"You kick the {target.name}, much to its annoyance!")


class Move(ActionWithDirection):
    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles[dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        self.entity.x, self.entity.y = dest_x, dest_y


class Bump(ActionWithDirection):
    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()
