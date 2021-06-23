from __future__ import annotations

import game.entity


class BaseComponent:
    entity: game.entity.Entity  # Owning entity instance.

    @property
    def engine(self) -> game.engine.Engine:
        return self.entity.gamemap.engine
