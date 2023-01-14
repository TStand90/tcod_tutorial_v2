from __future__ import annotations

import lzma
import pickle

import tcod
import random

import game.entity
import game.exceptions
import game.game_map
import game.message_log
import game.rendering


class Engine:
    game_map: game.game_map.GameMap
    game_world: game.game_map.GameWorld

    def __init__(self, player: game.entity.Actor):
        self.message_log = game.message_log.MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.rng = random.Random()

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
            self.game_map.tiles,
            (self.player.x, self.player.y),
            radius=8,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: tcod.Console) -> None:
        game.rendering.render_map(console, self.game_map)
        game.rendering.render_ui(console, self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
