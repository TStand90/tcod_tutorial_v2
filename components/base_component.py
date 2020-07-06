from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class BaseComponent:
    @property
    def parent(self) -> Entity:
        return self._parent

    @parent.setter
    def parent(self, parent: Entity) -> None:
        self._parent = parent
