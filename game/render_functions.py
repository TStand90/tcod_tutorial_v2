from __future__ import annotations

import tcod

import game.color
import game.engine
import game.game_map


def get_names_at_location(x: int, y: int, game_map: game.game_map.GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(entity.name for entity in game_map.entities if entity.x == x and entity.y == y)

    return names.capitalize()


def render_bar(console: tcod.Console, current_value: int, maximum_value: int, total_width: int) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=game.color.bar_empty)

    if bar_width > 0:
        console.draw_rect(x=0, y=45, width=bar_width, height=1, ch=1, bg=game.color.bar_filled)

    console.print(x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=game.color.bar_text)


def render_names_at_mouse_location(console: tcod.Console, x: int, y: int, engine: game.engine.Engine) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, game_map=engine.game_map)

    console.print(x=x, y=y, string=names_at_mouse_location)
