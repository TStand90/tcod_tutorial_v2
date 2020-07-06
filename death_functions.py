from __future__ import annotations

from typing import TYPE_CHECKING

from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


def check_for_dead_entities(engine: Engine) -> None:
    for entity in engine.game_map.actors:
        if entity.fighter.is_dead and entity.ai:
            kill_entity(engine, entity)


def kill_entity(engine: Engine, entity: Actor) -> None:
    if engine.player is entity:
        death_message = 'You died!'
        engine.event_handler = GameOverEventHandler(engine)
    else:
        death_message = f'{entity.name} is dead!'

    entity.char = "%"
    entity.color = (191, 0, 0)
    entity.blocks_movement = False
    entity.ai = None
    entity.name = f"remains of {entity.name}"
    entity.render_order = RenderOrder.CORPSE

    print(death_message)
