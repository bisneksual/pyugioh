from pyugioh.models import pydantic
from pyugioh.pygo_core import constants
from typing import Any

def get_class(card_type: str) -> pydantic.BaseCard:
    return \
             pydantic.SpellCard if "Spell " in card_type \
        else pydantic.TrapCard if "Trap " in card_type \
        else pydantic.SkillCard if "Skill " in card_type \
        else pydantic.TokenCard if "Token" in card_type \
        else pydantic.PendulumXDMonster if card_type in constants.PYUGIOH_TYPE_VALUES_PEND_EXTRA \
        else pydantic.ExtraDeckCard if card_type in constants.PYUGIOH_TYPE_VALUES_EXTRA \
        else pydantic.PendulumMonster if card_type in constants.PYUGIOH_TYPE_VALUES_PEND_MONSTER \
        else pydantic.MonsterCard if card_type in constants.PYUGIOH_TYPE_VALUES_MONSTER \
        else pydantic.BaseCard