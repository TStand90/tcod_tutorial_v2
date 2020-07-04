from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


class Action:
    def __init__(self, engine: Engine, entity: Actor) -> None:
        super().__init__()
        self.engine = engine
        self.entity = entity

    @property
    def context(self) -> Tuple[Engine, Actor]:
        """Return the engine and entity of this action.

        Useful to quickly create other actions."""
        return self.engine, self.entity

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class MouseMotionAction(Action):
    def __init__(self, engine: Engine, entity: Actor, tile_x: int, tile_y: int):
        super().__init__(engine, entity)

        self.tile_x = tile_x
        self.tile_y = tile_y

    def perform(self) -> bool:
        self.engine.mouse_location = (self.tile_x, self.tile_y)

        return False


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    def perform(self) -> bool:
        return True


class ActionWithDirection(Action):
    def __init__(self, engine: Engine, entity: Actor, dx: int, dy: int):
        super().__init__(engine, entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Actor]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> bool:
        target = self.blocking_entity

        if target and self.entity.fighter and target.fighter:
            self.entity.fighter.attack(self.engine, target)

            return True
        else:
            return False


class MovementAction(ActionWithDirection):
    def perform(self) -> bool:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return False  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return False  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return False  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)

        return True


class BumpAction(ActionWithDirection):
    def perform(self) -> bool:
        if self.blocking_entity:
            return MeleeAction(self.engine, self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.engine, self.entity, self.dx, self.dy).perform()
