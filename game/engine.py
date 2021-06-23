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

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: tcod.Console, context: tcod.context.Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()
