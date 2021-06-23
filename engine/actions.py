from __future__ import annotations

import engine.engine
import engine.entity


class Action:
    def perform(self, engine: engine.engine.Engine, entity: engine.entity.Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class Escape(Action):
    def perform(self, engine: engine.engine.Engine, entity: engine.entity.Entity) -> None:
        raise SystemExit()


class Move(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: engine.engine.Engine, entity: engine.entity.Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        entity.move(self.dx, self.dy)
