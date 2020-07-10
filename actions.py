from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
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

                    self.engine.turn_queue.schedule(interval=1, value=self.entity)

                    return
                else:
                    self.engine.message_log.add_message(f"Your inventory is full.")

                    self.engine.turn_queue.schedule(interval=0, value=self.entity)

                    return

        self.engine.message_log.add_message(f"There is nothing here to pick up.")

        self.engine.turn_queue.schedule(interval=0, value=self.entity)


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)
        self.item = item

    def perform(self) -> None:
        raise NotImplementedError()


class ConsumeItem(ItemAction):
    def perform(self) -> None:
        # Try consuming the item. It's possible the item cannot be consumed.
        item_consumed = self.item.consumable.consume(self.entity, self.engine)

        if item_consumed:
            self.entity.inventory.items.remove(self.item)

            self.engine.turn_queue.schedule(interval=1, value=self.entity)


class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)

        self.engine.turn_queue.schedule(interval=1, value=self.entity)


class WaitAction(Action):
    def perform(self) -> None:
        self.engine.turn_queue.schedule(interval=1, value=self.entity)


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

        self.engine.turn_queue.schedule(interval=1, value=self.entity)


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        # If the player tries an illegal move, it should not cost them a turn.
        # Enemies will lose a turn, otherwise, a never ending loop is possible.
        if self.entity == self.engine.player:
            default_interval = 0
        else:
            default_interval = 1

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            self.engine.turn_queue.schedule(interval=default_interval, value=self.entity)
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # return  # Destination is blocked by a tile.
            self.engine.turn_queue.schedule(interval=default_interval, value=self.entity)
            return
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            self.engine.turn_queue.schedule(interval=default_interval, value=self.entity)
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)

        self.engine.turn_queue.schedule(interval=1, value=self.entity)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
