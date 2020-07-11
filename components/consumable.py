from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    entity: Item

    def consume(self, consumer: Actor) -> bool:
        raise NotImplementedError()


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def consume(self, consumer: Actor) -> bool:
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.entity.name}, and recover {amount_recovered} HP!",
                (0, 255, 0),
            )
        else:
            raise Impossible(f"Your health is already full.")

        return amount_recovered > 0
