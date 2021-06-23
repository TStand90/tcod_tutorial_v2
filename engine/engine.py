from typing import Any, Iterable, Set

import tcod

import engine.entity
import engine.game_map
import engine.input_handlers


class Engine:
    def __init__(
        self,
        entities: Set[engine.entity.Entity],
        event_handler: engine.input_handlers.EventHandler,
        game_map: engine.game_map.GameMap,
        player: engine.entity.Entity,
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
