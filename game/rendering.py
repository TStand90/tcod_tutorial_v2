from __future__ import annotations

import numpy as np
import tcod

import game.game_map

tile_graphics = np.array(
    [
        (ord("#"), (0x80, 0x80, 0x80), (0x40, 0x40, 0x40)),  # wall
        (ord("."), (0x40, 0x40, 0x40), (0x18, 0x18, 0x18)),  # floor
    ],
    dtype=tcod.console.rgb_graphic,
)


def render_map(console: tcod.Console, gamemap: game.game_map.GameMap) -> None:
    console.rgb[0 : gamemap.width, 0 : gamemap.height] = tile_graphics[gamemap.tiles]

    for entity in gamemap.entities:
        console.print(entity.x, entity.y, entity.char, fg=entity.color)
