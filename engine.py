from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actor import Actor
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    game_map: GameMap
    player: Actor

    def __init__(self) -> None:
        self.event_handler = EventHandler(self)

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            if isinstance(entity, Actor):
                entity.ai.perform()

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

        context.present(console)

        console.clear()
