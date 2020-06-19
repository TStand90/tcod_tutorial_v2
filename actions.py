class Action:
    pass


class EscapeAction(Action):
    pass


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super(MovementAction, self).__init__()

        self.dx = dx
        self.dy = dy
