from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from components.ai import DeadAI
from death_functions import check_for_dead_entities
from entity import Actor
from game_map import GameMap
from input_handlers import InventoryEventHandler, MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_inventory_menu, render_names_at_mouse_location

if TYPE_CHECKING:
    from input_handlers import EventHandler


class Engine:
    def __init__(self, game_map: GameMap, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.game_map = game_map
        self.message_log = MessageLog(x=21, y=45, width=40, height=5)
        self.mouse_location = (0, 0)
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.actors - {self.player}:
            if entity.ai is not None and not isinstance(entity.ai, DeadAI):
                action = entity.ai.take_turn(self, self.player)

                if action is None:
                    continue

                action.perform()

        check_for_dead_entities(self)

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console)

        # If the current event handler is the Inventory handler, show the inventory screen.
        if isinstance(self.event_handler, InventoryEventHandler):
            render_inventory_menu(console=console, engine=self)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

        context.present(console)

        console.clear()
