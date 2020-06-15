import tcod

from actions import Action, ActionType
from input_handlers import handle_keys


def main():
    screen_width: int = 80
    screen_height: int = 50

    player_x: int = int(screen_width / 2)
    player_y: int = int(screen_height / 2)

    tcod.console_set_custom_font("arial10x10.png", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    with tcod.console_init_root(
            w=screen_width,
            h=screen_height,
            title="Yet Another Roguelike Tutorial",
            order="F",
            vsync=True
    ) as root_console:
        while True:
            root_console.print(x=player_x, y=player_y, string="@")

            tcod.console_flush()

            root_console.clear()

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()

                if event.type == "KEYDOWN":
                    action: [Action, None] = handle_keys(event.sym)

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
