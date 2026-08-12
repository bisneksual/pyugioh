from src.pyugioh import models
from src.pyugioh.pygo_core import constants
from typing import Any

def get_class(card_type: str) -> Any:
    return \
             models.SpellCard if "Spell " in card_type \
        else models.TrapCard if "Trap " in card_type \
        else models.SkillCard if "Skill " in card_type \
        else models.TokenCard if "Token" in card_type \
        else models.PendulumXDMonster if card_type in constants.PYUGIOH_TYPE_VALUES_PEND_EXTRA \
        else models.ExtraDeckCard if card_type in constants.PYUGIOH_TYPE_VALUES_EXTRA \
        else models.PendulumMonster if card_type in constants.PYUGIOH_TYPE_VALUES_PEND_MONSTER \
        else models.MonsterCard if card_type in constants.PYUGIOH_TYPE_VALUES_MONSTER \
        else models.BaseCard