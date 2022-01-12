from __future__ import annotations

import logging
import random

import tcod

import game.entity
import game.exceptions
import game.game_map
import game.message_log

logger = logging.getLogger(__name__)


class Engine:
    game_map: game.game_map.GameMap
    player: game.entity.Actor
    rng: random.Random
    mouse_location = (0, 0)

    def __init__(self) -> None:
        self.message_log = game.message_log.MessageLog()

    def handle_enemy_turns(self) -> None:
        logger.info("Enemy turn.")
        for entity in self.game_map.entities - {self.player}:
            if not isinstance(entity, game.entity.Actor):
                continue
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
        # If a tile is currently "visible" it will also be marked as "explored".
        self.game_map.explored |= self.game_map.visible
