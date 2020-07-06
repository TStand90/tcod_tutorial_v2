from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from death_functions import check_for_dead_entities
from entity import Actor
from game_map import GameMap
from input_handlers import MainGameEventHandler

if TYPE_CHECKING:
    from input_handlers import EventHandler


class Engine:
    def __init__(self, game_map: GameMap, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                action = entity.ai.take_turn(self)

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

        console.print(x=1, y=47, string=f'HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}')

        context.present(console)

        console.clear()
