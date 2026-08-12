import json
import re
from src.pyugioh.pygo_core import constants
from pydantic import BaseModel, field_validator,ValidationError, computed_field
from typing import Optional

class BaseCard(BaseModel):
    id: int
    name: str
    frame: str
    desc: str
    race: str
    set_code: Optional[str] = "N/A"

    def __init__(self,**data):
        data['frame'] = data.pop("frameType","N/A")
        super().__init__(**data)

class MonsterCard(BaseCard):
    type: str
    level: int
    attack: int
    defense: int

    @field_validator("type")
    @classmethod
    def validate_type(cls,v: str) -> str:
        if v not in constants.PYUGIOH_TYPE_VALUES_MONSTER:
            raise ValidationError(f"type must be one of the following: {constants.PYUGIOH_TYPE_VALUES_MONSTER}")
        return v

class PendulumMonster(MonsterCard):
    pend_desc: str
    scale: int

    def __init__(self, **data):
        __card_data = data
        __card_data['desc'] = __card_data.pop("monster_desc")
        super().__init__(**data)


class ExtraDeckCard(BaseCard):
    materials: Optional[str] = "N/A"

class PendulumXDMonster(ExtraDeckCard):
    m_desc: str
    pend_desc: str
    scale: int
    pass

class SpellCard(BaseCard):
    pass

class TrapCard(BaseCard):
    pass

class SkillCard(BaseCard):
    pass

class TokenCard(BaseCard):
    pass

__get_class = lambda card_type: \
    SpellCard if "Spell " in card_type \
    else TrapCard if "Trap " in card_type \
    else SkillCard if "Skill " in card_type \
    else TokenCard if "Token" in card_type \
    else PendulumXDMonster if card_type in constants.PYUGIOH_TYPE_VALUES_PEND_EXTRA \
    else ExtraDeckCard if card_type in constants.PYUGIOH_TYPE_VALUES_EXTRA \
    else PendulumMonster if card_type in constants.PYUGIOH_TYPE_VALUES_PEND_MONSTER \
    else MonsterCard if card_type in constants.PYUGIOH_TYPE_VALUES_MONSTER \
    else BaseCard

__sanitize_desc = lambda card_desc: card_desc.strip("'") ## strip double quotes from normal monster descriptions

__get_pend_desc = lambda card_desc: re.compile(constants.PYUGIOH_PEND_DESC_PATTERN).findall(card_desc)
__get_xd_mats = lambda card_desc: re.compile(constants.PYUGIOH_XD_MATS_PATTERN).findall(card_desc)

def __init_card() -> BaseCard:
    with open(".example/pend_xd.json","r") as fp:
        card_data = json.load(fp)
    if not isinstance(card_data,dict):
        exit()
    card_class = __get_class(card_data.get("type","N/A"))
    card = card_class.model_validate(card_data)
    return card

if __name__=="__main__":
    dark_magician = __init_card()
    print(type(dark_magician))
    print(dark_magician.model_dump())