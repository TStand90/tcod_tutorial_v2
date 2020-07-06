from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor
    from engine import Engine


class BaseComponent:
    entity: Actor  # Owning entity instance.

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine
