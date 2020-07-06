from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Actor


class BaseComponent:
    _parent: Actor

    @property
    def parent(self) -> Actor:
        return self._parent

    @parent.setter
    def parent(self, parent: Actor) -> None:
        self._parent = parent
