from __future__ import annotations

import game.engine
import game.entity
import game.game_map


class BaseComponent:
    parent: game.entity.Entity  # Owning entity instance.

    @property
    def gamemap(self) -> game.game_map.GameMap:
        return self.parent.gamemap

    @property
    def engine(self) -> game.engine.Engine:
        return self.gamemap.engine
