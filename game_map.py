from __future__ import annotations

from random import randint
from typing import Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

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

    def intersects(self, other: Rect) -> bool:
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

    def create_horizontal_tunnel(self, x1: int, x2: int, y: int) -> None:
        min_x = min(x1, x2)
        max_x = max(x1, x2) + 1

        self.tiles[min_x:max_x, y] = tile_types.floor

    def create_room(self, room: Rect) -> None:
        self.tiles[room.x1+1:room.x2, room.y1+1:room.y2] = tile_types.floor

    def create_vertical_tunnel(self, y1: int, y2: int, x: int) -> None:
        min_y = min(y1, y2)
        max_y = max(y1, y2) + 1

        self.tiles[x, min_y:max_y] = tile_types.floor

    def make_map(self, max_rooms: int, room_min_size: int, room_max_size: int, map_width: int, map_height: int,
                 player: Entity) -> None:
        rooms = []
        number_of_rooms = 0

        for r in range(max_rooms):
            width = randint(room_min_size, room_max_size)
            height = randint(room_min_size, room_max_size)

            x = randint(0, map_width - width - 1)
            y = randint(0, map_height - height - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, width, height)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersects(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center

                if number_of_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[number_of_rooms - 1].center

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y)
                        self.create_vertical_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                        self.create_horizontal_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                number_of_rooms += 1

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
