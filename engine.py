from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.fov_recompute = True
        self.fov_map = compute_fov(game_map.tiles["transparent"], (player.x, player.y), radius=8)
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        if self.fov_recompute:
            # Get the new FOV map based on the Player's current position
            self.fov_map = compute_fov(self.game_map.tiles["transparent"], (self.player.x, self.player.y), radius=8)

            # Set the "visible" tiles in the map to whatever is in the FOV map
            self.game_map.visible = self.fov_map

            # If a tile is in "visible", it should also be in "explored"
            self.game_map.explored |= self.game_map.visible

            self.fov_recompute = False

        self.game_map.render(console)

        for entity in self.entities:
            # Only render entities that are in the FOV
            if self.fov_map[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()
