from enum import auto, Enum


class ActionType(Enum):
    ESCAPE = auto()
    MOVEMENT = auto()


class Action:
    def __init__(self, action_type: ActionType, **kwargs):
        self.action_type: ActionType = action_type
        self.kwargs = kwargs
