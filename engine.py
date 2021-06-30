from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np 
from tcod.console import Console
from tcod.map import compute_fov
import tcod

import exceptions
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import (
    render_bar,
    render_names_at_mouse_location,
)

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def update_aoe(
        self, location: Tuple[int, int], radius: int, include_walls: bool = False,
    ) -> None:
        """Compute the blast area for an aoe action."""

        # Start with the fov from the center of the blast.
        self.game_map.aoe[:] = compute_fov(
            self.game_map.tiles["transparent"],
            location,
            radius=radius,
            light_walls=include_walls,
            algorithm=tcod.FOV_BASIC,
        )

        # Now limit the preview to visible tiles.
        it = np.nditer(
            [self.game_map.aoe, self.game_map.visible, None], flags=['buffered']
        )

        with it:
            for has_aoe, is_visible, tmp in it:
                tmp[...] = has_aoe and is_visible
            self.game_map.aoe = it.operands[2]

    def clear_aoe(self):
        # Clear out the aoe preview table.
        self.game_map.aoe.fill(False)

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
