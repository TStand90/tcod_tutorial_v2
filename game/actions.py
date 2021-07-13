from __future__ import annotations

import game.entity


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
        if not self.engine.game_map.tiles[dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        self.entity.x, self.entity.y = dest_x, dest_y
