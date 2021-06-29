from __future__ import annotations


class Action:
    pass


class Move(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
