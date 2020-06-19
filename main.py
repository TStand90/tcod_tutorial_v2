#!/usr/bin/env python3
import tcod

from actions import ActionType
from input_handlers import EventHandler


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
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

                if action is None:
                    continue

                action_type: ActionType = action.action_type

                if action_type == ActionType.MOVEMENT:
                    dx: int = action.kwargs.get("dx", 0)
                    dy: int = action.kwargs.get("dy", 0)

                    player_x += dx
                    player_y += dy
                elif action_type == ActionType.ESCAPE:
                    raise SystemExit()


if __name__ == "__main__":
    main()
