from __future__ import annotations

from random import randint
from typing import List, Tuple, TYPE_CHECKING

from game_map import GameMap
import tile_types


if TYPE_CHECKING:
    from entity import Entity


class Rect:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: Rect) -> bool:
        """Return True if this Rect overlaps with another Rect."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def create_horizontal_tunnel(gamemap: GameMap, x1: int, x2: int, y: int) -> None:
    min_x = min(x1, x2)
    max_x = max(x1, x2) + 1

    gamemap.tiles[min_x:max_x, y] = tile_types.floor


def create_vertical_tunnel(gamemap: GameMap, y1: int, y2: int, x: int) -> None:
    min_y = min(y1, y2)
    max_y = max(y1, y2) + 1

    gamemap.tiles[x, min_y:max_y] = tile_types.floor


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[Rect] = []

    for r in range(max_rooms):
        room_width = randint(room_min_size, room_max_size)
        room_height = randint(room_min_size, room_max_size)

        x = randint(0, dungeon.width - room_width - 1)
        y = randint(0, dungeon.height - room_height - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, room_width, room_height)

        # run through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # this room intersects, so go to the next attempt
        # if there are no intersections then the room is valid

        # dig out the rooms inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        # center coordinates of new room, will be useful later
        (new_x, new_y) = new_room.center

        if len(rooms) == 0:
            # this is the first room, where the player starts at
            player.x = new_x
            player.y = new_y
        else:
            # all rooms after the first:
            # connect it to the previous room with a tunnel

            # center coordinates of previous room
            (prev_x, prev_y) = rooms[-1].center

            # flip a coin (random number that is either 0 or 1)
            if randint(0, 1) == 1:
                # first move horizontally, then vertically
                create_horizontal_tunnel(dungeon, prev_x, new_x, prev_y)
                create_vertical_tunnel(dungeon, prev_y, new_y, new_x)
            else:
                # first move vertically, then horizontally
                create_vertical_tunnel(dungeon, prev_y, new_y, prev_x)
                create_horizontal_tunnel(dungeon, prev_x, new_x, new_y)

        # finally, append the new room to the list
        rooms.append(new_room)

    return dungeon
