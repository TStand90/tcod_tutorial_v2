from tcod.console import Console
from tcod.map import Map


class GameMap(Map):
    def __init__(self, width: int, height: int):
        super().__init__(width, height, order="F")

        self.walkable[:] = True

        self.walkable[30, 22] = False
        self.walkable[31, 22] = False
        self.walkable[32, 22] = False

    def render(self, console: Console):
        for y in range(self.height):
            for x in range(self.width):
                is_wall = not self.walkable[x, y]

                if is_wall:
                    console.print(x=x, y=y, string=' ', bg=(0, 0, 100))
                else:
                    console.print(x=x, y=y, string=' ', bg=(50, 50, 150))
