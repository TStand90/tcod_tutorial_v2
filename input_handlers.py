from typing import Optional

import tcod.event

from actions import Action, ActionType


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

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
