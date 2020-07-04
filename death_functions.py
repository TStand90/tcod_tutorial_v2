from __future__ import annotations

from typing import TYPE_CHECKING

from components.ai import DeadAI
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor


def check_for_dead_entities(engine: Engine) -> None:
    for entity in engine.game_map.actors:
        if entity.fighter and entity.fighter.is_dead and not isinstance(entity.ai, DeadAI):
            kill_entity(engine, entity)


def kill_entity(engine: Engine, entity: Actor) -> None:
    entity.char = '%'
    entity.color = (191, 0, 0)

    if engine.player == entity:
        death_message = 'You died!'
        death_message_color = (191, 0, 0)
        engine.event_handler = GameOverEventHandler(engine)
    else:
        death_message = f'{entity.name} is dead!'
        death_message_color = (255, 127, 0)
        entity.blocks_movement = False
        entity.ai = DeadAI()
        entity.name = f'remains of {entity.name}'
        entity.render_order = RenderOrder.CORPSE

    engine.message_log.add_message(death_message, death_message_color)
