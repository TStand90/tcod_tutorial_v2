from __future__ import annotations

import game.entity
import game.game_map


class Engine:
    game_map: game.game_map.GameMap
    player: game.entity.Entity
