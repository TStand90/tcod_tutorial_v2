from __future__ import annotations

from typing import Optional

import game.actions
import game.color
import game.components.inventory
import game.entity
import game.exceptions


class Consumable:
    parent: game.entity.Item

    def get_action(self, consumer: game.entity.Actor) -> Optional[game.actions.Action]:
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


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: game.actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.parent.gamemap.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                game.color.health_recovered,
            )
            self.consume()
        else:
            raise game.exceptions.Impossible("Your health is already full.")
