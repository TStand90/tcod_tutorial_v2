import tcod

import game.entity
import game.game_map
import game.input_handlers


class Engine:
    game_map: game.game_map.GameMap
    player: game.entity.Entity

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
