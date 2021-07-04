#!/usr/bin/env python3
import tcod

import game.engine
import game.entity
import game.game_map
import game.input_handlers


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet("data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    engine = game.engine.Engine()
    engine.game_map = game.game_map.GameMap(engine, map_width, map_height)
    engine.game_map.tiles[1:-1, 1:-1] = 1
    engine.game_map.tiles[30:33, 22] = 0
    engine.player = game.entity.Entity(engine.game_map, screen_width // 2, screen_height // 2, "@", (255, 255, 255))

    game.entity.Entity(engine.game_map, screen_width // 2 - 5, screen_height // 2, "@", (255, 255, 0))  # NPC

    event_handler = game.input_handlers.EventHandler(engine)

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            event_handler.on_render(console=root_console)
            context.present(root_console)

            for event in tcod.event.wait():
                event_handler = event_handler.handle_events(event)


if __name__ == "__main__":
    main()
