from typing import Optional

import tcod.event

from actions import Action, ActionType


def handle_keys(key: int) -> Optional[Action]:
    action: Optional[Action] = None

    if key == tcod.event.K_UP:
        action = Action(ActionType.MOVEMENT, dx=0, dy=-1)
    elif key == tcod.event.K_DOWN:
        action = Action(ActionType.MOVEMENT, dx=0, dy=1)
    elif key == tcod.event.K_LEFT:
        action = Action(ActionType.MOVEMENT, dx=-1, dy=0)
    elif key == tcod.event.K_RIGHT:
        action = Action(ActionType.MOVEMENT, dx=1, dy=0)

    elif key == tcod.event.K_ESCAPE:
        action = Action(ActionType.ESCAPE)

    # No valid key was pressed
    return action
