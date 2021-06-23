#!/usr/bin/env python3
import copy

import tcod

import engine.engine
import engine.entity
import engine.entity_factories
import engine.game_map
import engine.input_handlers
import engine.procgen


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("data/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = engine.input_handlers.EventHandler()

    player = copy.deepcopy(engine.entity_factories.player)

    game_map = engine.procgen.generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        player=player,
    )

    engine_ = engine.engine.Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine_.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine_.handle_events(events)


if __name__ == "__main__":
    main()
