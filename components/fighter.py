from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def attack(self, target: Actor) -> None:
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            print(f'{self.parent.name.capitalize()} attacks {target.name} for {damage} hit points.')
        else:
            print(f'{self.parent.name.capitalize()} attacks {target.name} but does no damage.')

    @property
    def is_dead(self) -> bool:
        return self.hp <= 0

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
