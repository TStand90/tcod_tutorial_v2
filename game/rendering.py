from __future__ import annotations

import numpy as np
import tcod

import game.engine
import game.game_map
import game.render_functions

tile_graphics = np.array(
    [
        (ord("#"), (0x80, 0x80, 0x80), (0x40, 0x40, 0x40)),  # wall
        (ord("."), (0x40, 0x40, 0x40), (0x18, 0x18, 0x18)),  # floor
    ],
    dtype=tcod.console.rgb_graphic,
)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=tcod.console.rgb_graphic)


def render_map(console: tcod.Console, gamemap: game.game_map.GameMap) -> None:
    # The default graphics are of tiles that are visible.
    light = tile_graphics[gamemap.tiles]

    # Apply effects to create a darkened map of tile graphics.
    dark = light.copy()
    dark["fg"] //= 2
    dark["bg"] //= 8

    # If a tile is in the "visible" array, then draw it with the "light" colors.
    # If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
    # Otherwise, the default graphic is "SHROUD".
    console.rgb[0 : gamemap.width, 0 : gamemap.height] = np.select(
        condlist=[gamemap.visible, gamemap.explored],
        choicelist=[light, dark],
        default=SHROUD,
    )

    for entity in sorted(gamemap.entities, key=lambda x: x.render_order.value):
        if not gamemap.visible[entity.x, entity.y]:
            continue  # Skip entities that are not in the FOV.
        console.print(entity.x, entity.y, entity.char, fg=entity.color)


def render_ui(console: tcod.Console, engine: game.engine.Engine) -> None:
    engine.message_log.render(console=console, x=21, y=45, width=40, height=5)

    game.render_functions.render_bar(
        console=console,
        current_value=engine.player.fighter.hp,
        maximum_value=engine.player.fighter.max_hp,
        total_width=20,
    )

    game.render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=engine)
