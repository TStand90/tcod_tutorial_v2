from typing import Any, Iterable, Set

import tcod

import game.entity
import game.game_map
import game.input_handlers


class Engine:
    def __init__(
        self,
        entities: Set[game.entity.Entity],
        event_handler: game.input_handlers.EventHandler,
        game_map: game.game_map.GameMap,
        player: game.entity.Entity,
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()  # Update the FOV before the players next action.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = tcod.map.compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: tcod.Console, context: tcod.context.Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()
