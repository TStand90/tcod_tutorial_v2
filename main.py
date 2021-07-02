#!/usr/bin/env python3
import tcod

MOVE_KEYS = {
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
}


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x: int = screen_width // 2
    player_y: int = screen_height // 2

    tileset = tcod.tileset.load_tilesheet("data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

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
            root_console.print(x=player_x, y=player_y, string="@")
            context.present(root_console)

            for event in tcod.event.wait():
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit(0)
                if isinstance(event, tcod.event.KeyDown):
                    if event.sym in MOVE_KEYS:
                        delta_x, delta_y = MOVE_KEYS[event.sym]
                        dest_x = player_x + delta_x
                        dest_y = player_y + delta_y
                        if 0 <= dest_x < screen_width and 0 <= dest_y < screen_height:
                            player_x, player_y = dest_x, dest_y


if __name__ == "__main__":
    main()
