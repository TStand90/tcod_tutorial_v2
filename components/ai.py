from __future__ import annotations

import math
from typing import TYPE_CHECKING

from actions import MeleeAction, MovementAction, WaitAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from actions import Action
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseAI(BaseComponent):
    def take_turn(self, engine: Engine) -> Action:
        raise NotImplementedError()


class HostileEnemy(BaseAI):
    def take_turn(self, engine: Engine) -> Action:
        target = engine.player
        dx = target.x - self.parent.x
        dy = target.y - self.parent.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        action: Action = WaitAction(self.parent)

        if engine.game_map.visible[self.parent.x, self.parent.y]:
            if distance >= 2:
                destination_x, destination_y = self.parent.get_first_step_towards_destination(target.x, target.y,
                                                                                              engine.game_map)
                action = MovementAction(self.parent, destination_x - self.parent.x, destination_y - self.parent.y)
            else:
                action = MeleeAction(self.parent, dx, dy)

        return action
