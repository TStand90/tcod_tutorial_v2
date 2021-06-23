from __future__ import annotations

from typing import Iterable, Iterator, Optional

import numpy as np
import tcod

import engine.engine
import engine.entity
import engine.tiles


class GameMap:
    def __init__(
        self, engine_: engine.engine.Engine, width: int, height: int, entities: Iterable[engine.entity.Entity] = ()
    ):
        self.engine = engine_
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=engine.tiles.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    @property
    def actors(self) -> Iterator[engine.entity.Actor]:
        """Iterate over this maps living actors."""
        yield from (entity for entity in self.entities if isinstance(entity, engine.entity.Actor) and entity.is_alive)

    def get_blocking_entity_at_location(
        self,
        location_x: int,
        location_y: int,
    ) -> Optional[engine.entity.Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[engine.entity.Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: tcod.Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=engine.tiles.SHROUD,
        )

        entities_sorted_for_rendering = sorted(self.entities, key=lambda x: x.render_order.value)

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
