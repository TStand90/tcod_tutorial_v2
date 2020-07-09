from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> bool:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> bool:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                item_added = self.entity.inventory.add_item(item)

                if item_added:
                    self.engine.game_map.entities.remove(item)
                    self.engine.message_log.add_message(
                        f"You picked up the {item.name}!"
                    )

                    return True
                else:
                    self.engine.message_log.add_message(f"Your inventory is full.")

                    return False

        self.engine.message_log.add_message(f"There is nothing here to pick up.")

        return False


class MenuSelectAction(Action):
    def __init__(self, entity: Actor, index: int):
        super().__init__(entity)

        self.index = index

    def perform(self) -> bool:
        from input_handlers import MainGameEventHandler, InventoryEventHandler

        try:
            # Get the item at the index the player selected
            selected_item = self.entity.inventory.items[self.index]

            # Check if the player is trying to consume or drop an item, which can be determined by looking at the
            # "dropping" attribute in the event handler class.
            if (
                isinstance(self.engine.event_handler, InventoryEventHandler)
                and self.engine.event_handler.dropping
            ):
                self.entity.inventory.drop(selected_item, self.engine)

                # Switch the event handler back to the main game, so the inventory menu closes.
                self.engine.event_handler = MainGameEventHandler(engine=self.engine)

                # Dropping an item takes a turn.
                return True
            elif selected_item.consumable:
                # Try consuming the item. It's possible the item cannot be consumed.
                item_consumed = selected_item.consumable.consume(
                    self.entity, self.engine
                )

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
    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

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

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return  # No entity to attack.

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
