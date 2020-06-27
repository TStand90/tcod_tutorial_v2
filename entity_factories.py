from entity import Entity


def create_orc(x: int, y: int) -> Entity:
    return Entity(x=x, y=y, char="o", color=(63, 127, 63), name="Orc", blocks_movement=True)


def create_player(x: int, y: int) -> Entity:
    return Entity(x=x, y=y, char="@", color=(255, 255, 255), name="Player", blocks_movement=True)


def create_troll(x: int, y: int) -> Entity:
    return Entity(x=x, y=y, char="T", color=(0, 127, 0), name="Troll", blocks_movement=True)
