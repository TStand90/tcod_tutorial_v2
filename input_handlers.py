from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
