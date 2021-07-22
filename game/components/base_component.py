from __future__ import annotations

import game.entity


class BaseComponent:
    entity: game.entity.Actor  # Owning entity instance.
