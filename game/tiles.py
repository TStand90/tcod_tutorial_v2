from __future__ import annotations

from typing import Any, Tuple

import numpy as np
import tcod
from numpy.typing import NDArray

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", tcod.console.rgb_graphic),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> NDArray[Any]:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)))
wall = new_tile(walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)))
