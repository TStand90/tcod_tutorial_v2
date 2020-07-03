from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        raise NotImplementedError()


class MainGameEventHandler(EventHandler):
    def handle_events(self) -> None:
        from death_functions import check_for_dead_entities

        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            check_for_dead_entities(self.engine)

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        # Common arguments for player actions.
        context = (self.engine, self.engine.player)

        if key == tcod.event.K_UP:
            action = BumpAction(*context, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(*context, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(*context, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(*context, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(*context)

        # No valid key was pressed
        return action


class GameOverEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(self.engine, self.engine.player)

            # No valid key was pressed
        return action
