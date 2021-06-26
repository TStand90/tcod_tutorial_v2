#!/usr/bin/env python3
import tcod

import game.actions
import game.input_handlers


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet("data/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = game.input_handlers.EventHandler()

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            context.present(root_console)

            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if isinstance(action, game.actions.Move):
                    new_x = player_x + action.dx
                    new_y = player_y + action.dy
                    if 0 <= new_x < screen_width and 0 <= new_y < screen_height:
                        player_x, player_y = new_x, new_y


if __name__ == "__main__":
    main()
