from typing import Optional

import tcod.event

import game.actions


class EventHandler(tcod.event.EventDispatch[game.actions.Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[game.actions.Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[game.actions.Action]:
        action: Optional[game.actions.Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = game.actions.Bump(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = game.actions.Bump(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = game.actions.Bump(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = game.actions.Bump(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = game.actions.Escape()

        # No valid key was pressed
        return action
