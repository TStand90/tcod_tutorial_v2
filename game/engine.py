from __future__ import annotations

import tcod

import game.entity
import game.exceptions
import game.game_map
import game.input_handlers
import game.message_log
import game.render_functions


class Engine:
    game_map: game.game_map.GameMap

    def __init__(self, player: game.entity.Actor):
        self.event_handler: game.input_handlers.EventHandler = game.input_handlers.MainGameEventHandler(self)
        self.message_log = game.message_log.MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except game.exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = tcod.map.compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: tcod.Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        game.render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        game.render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
