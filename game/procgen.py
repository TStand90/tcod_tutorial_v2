from __future__ import annotations

from typing import Iterator, List, Tuple

import tcod

import game.components.consumable
import game.engine
import game.entity
import game.game_map
from game.components.ai import HostileEnemy
from game.components.fighter import Fighter

WALL = 0
FLOOR = 1


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Return the center coordinates of the room."""
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


def place_entities(
    room: RectangularRoom, dungeon: game.game_map.GameMap, maximum_monsters: int, maximum_items: int
) -> None:
    rng = dungeon.engine.rng
    number_of_monsters = rng.randint(0, maximum_monsters)
    number_of_items = rng.randint(0, maximum_items)

    for _ in range(number_of_monsters):
        x = rng.randint(room.x1 + 1, room.x2 - 1)
        y = rng.randint(room.y1 + 1, room.y2 - 1)

        if dungeon.get_blocking_entity_at(x, y):
            continue
        if (x, y) == dungeon.enter_xy:
            continue

        if rng.random() < 0.8:
            game.entity.Actor(
                dungeon,
                x,
                y,
                char="o",
                color=(63, 127, 63),
                name="Orc",
                ai_cls=HostileEnemy,
                fighter=Fighter(hp=10, defense=0, power=3),
            )
        else:
            game.entity.Actor(
                dungeon,
                x,
                y,
                char="T",
                color=(0, 127, 0),
                name="Troll",
                ai_cls=HostileEnemy,
                fighter=Fighter(hp=16, defense=1, power=4),
            )

    for _ in range(number_of_items):
        x = rng.randint(room.x1 + 1, room.x2 - 1)
        y = rng.randint(room.y1 + 1, room.y2 - 1)

        game.entity.Item(
            dungeon,
            x,
            y,
            char="!",
            color=(127, 0, 255),
            name="Health Potion",
            consumable=game.components.consumable.HealingConsumable(amount=4),
        )


def tunnel_between(
    engine: game.engine.Engine, start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if engine.rng.random() < 0.5:  # 50% chance.
        corner_x, corner_y = x2, y1  # Move horizontally, then vertically.
    else:
        corner_x, corner_y = x1, y2  # Move vertically, then horizontally.

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    max_items_per_room: int,
    engine: game.engine.Engine,
) -> game.game_map.GameMap:
    """Generate a new dungeon map."""
    dungeon = game.game_map.GameMap(engine, map_width, map_height)

    rooms: List[RectangularRoom] = []

    for _ in range(max_rooms):
        room_width = engine.rng.randint(room_min_size, room_max_size)
        room_height = engine.rng.randint(room_min_size, room_max_size)

        x = engine.rng.randint(0, dungeon.width - room_width - 1)
        y = engine.rng.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with.
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = FLOOR

        if len(rooms) == 0:
            # The first room, where the player starts.
            dungeon.enter_xy = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(engine, rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = FLOOR

        place_entities(new_room, dungeon, max_monsters_per_room, max_items_per_room)

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon
