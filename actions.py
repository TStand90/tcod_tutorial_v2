from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

from entity import Actor

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def __init__(self, engine: Engine, entity: Entity):
        super().__init__()
        self.engine = engine
        self.entity = entity

    @property
    def context(self) -> Tuple[Engine, Entity]:
        """Return the engine and entity of this action.

        Useful to quickly create other actions."""
        return self.engine, self.entity

    def perform(self) -> bool:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class MouseMotionAction(Action):
    def __init__(self, engine: Engine, entity: Entity, tile_x: int, tile_y: int):
        super().__init__(engine, entity)

        self.tile_x = tile_x
        self.tile_y = tile_y

    def perform(self) -> bool:
        self.engine.mouse_location = (self.tile_x, self.tile_y)

        return False


class PickupAction(Action):
    def __init__(self, engine: Engine, entity: Actor):
        super().__init__(engine, entity)

    def perform(self) -> bool:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y and isinstance(self.entity, Actor):
                item_added = self.entity.inventory.add_item(item)

                if item_added:
                    self.engine.game_map.entities.remove(item)
                    self.engine.message_log.add_message(f"You picked up the {item.name}!")

                    return True
                else:
                    self.engine.message_log.add_message(f"Your inventory is full.")

                    return False

        self.engine.message_log.add_message(f"There is nothing here to pick up.")

        return False


class MenuSelectAction(Action):
    def __init__(self, engine: Engine, entity: Actor, index: int):
        super().__init__(engine, entity)

        self.index = index

    def perform(self) -> bool:
        from input_handlers import MainGameEventHandler, InventoryEventHandler

        if not isinstance(self.entity, Actor):
            return False

        try:
            # Get the item at the index the player selected
            selected_item = self.entity.inventory.items[self.index]

            # Check if the player is trying to consume or drop an item, which can be determined by looking at the
            # "dropping" attribute in the event handler class.
            if isinstance(self.engine.event_handler, InventoryEventHandler) and self.engine.event_handler.dropping:
                self.entity.inventory.drop(selected_item, self.engine)

                # Switch the event handler back to the main game, so the inventory menu closes.
                self.engine.event_handler = MainGameEventHandler(engine=self.engine)

                # Dropping an item takes a turn.
                return True
            elif selected_item.consumable:
                # Try consuming the item. It's possible the item cannot be consumed.
                item_consumed = selected_item.consumable.consume(self.entity, self.engine)

                if item_consumed:
                    # Remove the item from the inventory.
                    self.entity.inventory.items.remove(selected_item)

                    # Switch the event handler back to the main game, so the inventory menu closes.
                    self.engine.event_handler = MainGameEventHandler(engine=self.engine)

                    # Consuming an item takes a turn.
                    return True
        except IndexError:
            self.engine.message_log.add_message("Invalid entry.", (255, 255, 0))

        # An item was not consumed, so don't make a turn pass.
        return False


class ShowInventoryAction(Action):
    def __init__(self, engine: Engine, entity: Entity, dropping: bool = False):
        super().__init__(engine, entity)

        self.dropping = dropping  # Denotes if the player is trying to drop an item or not

    def perform(self) -> bool:
        from input_handlers import InventoryEventHandler

        # Set the event handler to the one that handles the inventory.
        self.engine.event_handler = InventoryEventHandler(engine=self.engine, dropping=self.dropping)

        # Opening the menu does not consume a turn.
        return False


class EscapeAction(Action):
    def perform(self) -> bool:
        from input_handlers import InventoryEventHandler

        if isinstance(self.engine.event_handler, InventoryEventHandler):
            from input_handlers import MainGameEventHandler

            self.engine.event_handler = MainGameEventHandler(engine=self.engine)
        else:
            raise SystemExit()

        return False


class WaitAction(Action):
    def perform(self) -> bool:
        return True


class ActionWithDirection(Action):
    def __init__(self, engine: Engine, entity: Entity, dx: int, dy: int):
        super().__init__(engine, entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    def perform(self) -> bool:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> bool:
        target = self.blocking_entity

        if target and isinstance(self.entity, Actor) and isinstance(target, Actor) and self.entity.fighter\
                and target.fighter:
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
