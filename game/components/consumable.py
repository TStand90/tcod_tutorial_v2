from __future__ import annotations

from typing import Optional

from game.components.base_component import BaseComponent
import game.actions
import game.color
import game.components.ai
import game.components.inventory
import game.entity
import game.exceptions
import game.input_handlers


class Consumable(BaseComponent):
    parent: game.entity.Item

    def get_action(self, consumer: game.entity.Actor) -> Optional[game.input_handlers.ActionOrHandler]:
        """Try to return the action for this item."""
        return game.actions.ItemAction(consumer, self.parent)

    def activate(self, action: game.actions.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, game.components.inventory.Inventory):
            inventory.items.remove(entity)


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: game.entity.Actor) -> game.input_handlers.SingleRangedAttackHandler:
        self.engine.message_log.add_message("Select a target location.", game.color.needs_target)
        return game.input_handlers.SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: game.actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: game.actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise game.exceptions.Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise game.exceptions.Impossible("You must select an enemy to target.")
        if target is consumer:
            raise game.exceptions.Impossible("You cannot confuse yourself!")

        self.engine.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            game.color.status_effect_applied,
        )
        target.ai = game.components.ai.ConfusedEnemy(
            entity=target,
            previous_ai=target.ai,
            turns_remaining=self.number_of_turns,
        )
        self.consume()


class FireballDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: game.entity.Actor) -> game.input_handlers.AreaRangedAttackHandler:
        self.engine.message_log.add_message("Select a target location.", game.color.needs_target)
        return game.input_handlers.AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: game.actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: game.actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise game.exceptions.Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise game.exceptions.Impossible("There are no targets in the radius.")
        self.consume()


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: game.actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                game.color.health_recovered,
            )
            self.consume()
        else:
            raise game.exceptions.Impossible("Your health is already full.")


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: game.actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise game.exceptions.Impossible("No enemy is close enough to strike.")
