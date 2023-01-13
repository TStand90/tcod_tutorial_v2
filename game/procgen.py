from __future__ import annotations

from typing import Dict, Iterator, List, Tuple
import random

import tcod

import game.engine
import game.entity
import game.entity_factories
import game.game_map

WALL = 0
FLOOR = 1
DOWN_STAIRS = 2

max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[game.entity.Entity, int]]] = {
    0: [(game.entity_factories.health_potion, 35)],
    2: [(game.entity_factories.confusion_scroll, 10)],
    4: [(game.entity_factories.lightning_scroll, 25), (game.entity_factories.sword, 5)],
    6: [(game.entity_factories.fireball_scroll, 25), (game.entity_factories.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[game.entity.Entity, int]]] = {
    0: [(game.entity_factories.orc, 80)],
    3: [(game.entity_factories.troll, 15)],
    5: [(game.entity_factories.troll, 30)],
    7: [(game.entity_factories.troll, 60)],
}


def get_max_value_for_floor(max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
    rng: random.Random,
    weighted_chances_by_floor: Dict[int, List[Tuple[game.entity.Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[game.entity.Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = rng.choices(entities, weights=entity_weighted_chance_values, k=number_of_entities)

    return chosen_entities


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


def place_entities(room: RectangularRoom, dungeon: game.game_map.GameMap, floor_number: int) -> None:
    rng = dungeon.engine.rng
    number_of_monsters = rng.randint(0, get_max_value_for_floor(max_monsters_by_floor, floor_number))
    number_of_items = rng.randint(0, get_max_value_for_floor(max_items_by_floor, floor_number))

    monsters: List[game.entity.Entity] = get_entities_at_random(rng, enemy_chances, number_of_monsters, floor_number)
    items: List[game.entity.Entity] = get_entities_at_random(rng, item_chances, number_of_items, floor_number)

    for entity in monsters + items:
        x = rng.randint(room.x1 + 1, room.x2 - 1)
        y = rng.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


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
    engine: game.engine.Engine,
) -> game.game_map.GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = game.game_map.GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for _ in range(max_rooms):
        room_width = engine.rng.randint(room_min_size, room_max_size)
        room_height = engine.rng.randint(room_min_size, room_max_size)

        x = engine.rng.randint(0, dungeon.width - room_width - 1)
        y = engine.rng.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = FLOOR

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(engine, rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = FLOOR

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = DOWN_STAIRS
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon
