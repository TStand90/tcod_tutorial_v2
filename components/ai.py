from __future__ import annotations

import math

from actions import Action, MeleeAction, MovementAction, WaitAction
from components.base_component import BaseComponent


class BaseAI(Action, BaseComponent):
    def perform(self) -> None:
        raise NotImplementedError()


class HostileEnemy(BaseAI):
    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        action: Action = WaitAction(self.entity)

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance >= 2:
                dest_x, dest_y = self.entity.get_path_astar(target.x, target.y)[0]
                action = MovementAction(
                    self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
                )
            else:
                action = MeleeAction(self.entity, dx, dy)

        return action.perform()
