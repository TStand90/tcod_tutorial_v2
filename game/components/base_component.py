from __future__ import annotations

import game.engine
import game.entity
import game.game_map


class BaseComponent:
    entity: game.entity.Actor  # Owning entity instance.

    @property
    def parent(self) -> game.entity.Actor:
        return self.entity

    @property
    def gamemap(self) -> game.game_map.GameMap:
        return self.parent.gamemap

    @property
    def engine(self) -> game.engine.Engine:
        return self.gamemap.engine
