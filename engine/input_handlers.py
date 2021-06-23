from typing import Optional

import tcod.event

import engine.actions


class EventHandler(tcod.event.EventDispatch[engine.actions.Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[engine.actions.Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[engine.actions.Action]:
        action: Optional[engine.actions.Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = engine.actions.Bump(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = engine.actions.Bump(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = engine.actions.Bump(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = engine.actions.Bump(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = engine.actions.Escape()

        # No valid key was pressed
        return action
