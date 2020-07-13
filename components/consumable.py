from __future__ import annotations

from typing import TYPE_CHECKING

import color
import components.ai
from components.base_component import BaseComponent
from exceptions import NeedsTargetException, Impossible
from input_handlers import (
    InventoryEventHandler,
    AreaRangedAttackHandler,
    SingleRangedAttackHandler,
)

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def consume(self, consumer: Actor) -> None:
        raise NotImplementedError()


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def consume(self, consumer: Actor) -> None:
        if isinstance(self.engine.event_handler, InventoryEventHandler):
            self.engine.event_handler = SingleRangedAttackHandler(
                engine=self.engine, callback=self.consume
            )

            raise NeedsTargetException("Select a target location.")
        else:
            target_position = self.engine.mouse_location

            if target_position:
                target_x, target_y = target_position

                if not self.engine.game_map.visible[target_x, target_y]:
                    raise Impossible("You cannot target an area that you cannot see.")

                actor = self.engine.game_map.get_actor_at_location(target_x, target_y)

                if actor:
                    if actor == consumer:
                        raise Impossible("You cannot confuse yourself!")
                    else:
                        self.engine.message_log.add_message(
                            f"The eyes of the {actor.name} look vacant, as it starts to stumble around!",
                            color.status_effect_applied,
                        )
                        actor.ai = components.ai.ConfusedEnemy(
                            entity=actor,
                            previous_ai=actor.ai,
                            turns_remaining=self.number_of_turns,
                        )
                else:
                    raise Impossible("You must select an enemy to target.")


class FireballDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def consume(self, consumer: Actor) -> None:
        if isinstance(self.engine.event_handler, InventoryEventHandler):
            self.engine.event_handler = AreaRangedAttackHandler(
                engine=self.engine, radius=self.radius, callback=self.consume
            )

            raise NeedsTargetException("Select a target location.")
        else:
            target_position = self.engine.mouse_location

            if target_position:
                target_x, target_y = target_position

                if not self.engine.game_map.visible[target_x, target_y]:
                    raise Impossible("You cannot target an area that you cannot see.")

                targets_hit = False

                for actor in self.engine.game_map.actors:
                    if actor.distance(*target_position) <= self.radius:
                        self.engine.message_log.add_message(
                            f"The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!"
                        )
                        actor.fighter.take_damage(self.damage)
                        targets_hit = True

                if not targets_hit:
                    raise Impossible("There are no targets in the radius.")


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def consume(self, consumer: Actor) -> None:
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                (0, 255, 0),
            )
        else:
            raise Impossible(f"Your health is already full.")


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def consume(self, consumer: Actor) -> None:
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if (
                actor.fighter
                and actor != consumer
                and self.parent.gamemap.visible[actor.x, actor.y]
            ):
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
            )
            target.fighter.take_damage(self.damage)
        else:
            raise Impossible("No enemy is close enough to strike.")
