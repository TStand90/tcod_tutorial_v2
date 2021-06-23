from __future__ import annotations

import engine.entity


class BaseComponent:
    entity: engine.entity.Entity  # Owning entity instance.

    @property
    def engine_(self) -> engine.engine.Engine:
        return self.entity.gamemap.engine
