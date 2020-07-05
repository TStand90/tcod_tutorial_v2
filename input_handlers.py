from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
from tcod.context import Context

from actions import Action, BumpAction, EscapeAction, MenuSelectAction, MouseMotionAction, PickupAction,\
    ShowInventoryAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, context: Context) -> None:
        raise NotImplementedError()

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> Optional[Action]:
        action = MouseMotionAction(self.engine, self.engine.player, tile_x=event.tile.x, tile_y=event.tile.y)

        return action


class InventoryEventHandler(EventHandler):
    def __init__(self, engine: Engine, dropping: bool = False):
        super().__init__(engine)

        self.dropping = dropping

    def handle_events(self, context: Context) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            turn_passed = action.perform()

            if turn_passed:
                self.engine.handle_enemy_turns()

            self.engine.update_fov()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(engine=self.engine, entity=self.engine.player)
        else:
            index = key - ord("a")

            if 0 <= index <= 26:
                action = MenuSelectAction(engine=self.engine, entity=self.engine.player, index=index)

        return action


class MainGameEventHandler(EventHandler):
    def handle_events(self, context: Context) -> None:
        from death_functions import check_for_dead_entities

        for event in tcod.event.wait():
            context.convert_event(event)

            action = self.dispatch(event)

            if action is None:
                continue

            turn_passed = action.perform()

            check_for_dead_entities(self.engine)

            if turn_passed:
                self.engine.handle_enemy_turns()

            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        # Common arguments for player actions.
        context = (self.engine, self.engine.player)

        if key in (tcod.event.K_UP, tcod.event.K_k):
            action = BumpAction(*context, dx=0, dy=-1)
        elif key in (tcod.event.K_DOWN, tcod.event.K_j):
            action = BumpAction(*context, dx=0, dy=1)
        elif key in (tcod.event.K_LEFT, tcod.event.K_h):
            action = BumpAction(*context, dx=-1, dy=0)
        elif key in (tcod.event.K_RIGHT, tcod.event.K_l):
            action = BumpAction(*context, dx=1, dy=0)
        elif key == tcod.event.K_y:
            action = BumpAction(*context, dx=-1, dy=-1)
        elif key == tcod.event.K_u:
            action = BumpAction(*context, dx=1, dy=-1)
        elif key == tcod.event.K_b:
            action = BumpAction(*context, dx=-1, dy=1)
        elif key == tcod.event.K_n:
            action = BumpAction(*context, dx=1, dy=1)
        elif key == tcod.event.K_PERIOD:
            action = WaitAction(*context)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(*context)

        elif key == tcod.event.K_g:
            action = PickupAction(*context)

        elif key == tcod.event.K_i:
            action = ShowInventoryAction(*context)

        elif key == tcod.event.K_d:
            action = ShowInventoryAction(*context, dropping=True)

        # No valid key was pressed
        return action


class GameOverEventHandler(EventHandler):
    def handle_events(self, context: Context) -> None:
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
