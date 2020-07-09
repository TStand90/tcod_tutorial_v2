from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Item


class Consumable(BaseComponent):
    entity: Item

    def consume(self, consumer: Actor, engine: Engine) -> bool:
        raise NotImplementedError()


class HealthPotion(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def consume(self, consumer: Actor, engine: Engine) -> bool:
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            engine.message_log.add_message(
                f"You consume the health potion, and recover {amount_recovered} HP!",
                (0, 255, 0),
            )
        else:
            engine.message_log.add_message(f"Your health is already full.")

        return amount_recovered > 0
