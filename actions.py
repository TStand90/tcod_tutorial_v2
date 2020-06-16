from enum import auto, Enum
from typing import Any


class ActionType(Enum):
    ESCAPE = auto()
    MOVEMENT = auto()


class Action:
    def __init__(self, action_type: ActionType, **kwargs: Any):
        self.action_type = action_type
        self.kwargs = kwargs
