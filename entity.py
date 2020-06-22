from typing import Tuple

from tcod.console import Console


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def render(self, console: Console):
        console.print(x=self.x, y=self.y, string=self.char, fg=self.color)
