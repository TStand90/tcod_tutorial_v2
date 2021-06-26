from __future__ import annotations

import game.engine
import game.entity


class Action:
    def __init__(self, entity: game.entity.Entity) -> None:
        super().__init__()
        self.entity = entity
        self.engine = entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class Escape(Action):
    def perform(self) -> None:
        raise SystemExit()


class Move(Action):
    def __init__(self, entity: game.entity.Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        dest_x = self.entity.x + self.dx
        dest_y = self.entity.y + self.dy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        self.entity.move(self.dx, self.dy)
