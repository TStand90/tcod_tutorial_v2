#!/usr/bin/env python3
import tcod

import engine.engine
import engine.entity
import engine.game_map
import engine.input_handlers


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet("data/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = engine.input_handlers.EventHandler()

    player = engine.entity.Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = engine.entity.Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = engine.game_map.GameMap(map_width, map_height)

    engine_ = engine.engine.Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

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
