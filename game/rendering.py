from __future__ import annotations

import numpy as np
import tcod

import game.game_map

wall = np.array((ord("#"), (0x80, 0x80, 0x80), (0x40, 0x40, 0x40)), dtype=tcod.console.rgb_graphic)
floor = np.array((ord("."), (0x40, 0x40, 0x40), (0x20, 0x20, 0x20)), dtype=tcod.console.rgb_graphic)


def render_map(console: tcod.Console, gamemep: game.game_map.GameMap) -> None:
    console.rgb[0 : gamemep.width, 0 : gamemep.height] = np.where(gamemep.tiles, floor, wall)

    for entity in gamemep.entities:
        console.print(entity.x, entity.y, entity.char, fg=entity.color)
