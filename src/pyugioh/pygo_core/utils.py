import re
from src.pyugioh.pygo_core import constants
from src.pyugioh import models
from typing import Any
import json

def sanitize_desc(card_desc:str) -> str:
    return card_desc.strip("'") ## strip double quotes from normal monster descriptions

def get_pend_desc(card_desc:str) -> str:
    return re.compile(constants.PYUGIOH_PEND_DESC_PATTERN).findall(card_desc)

def get_xd_mats(card_desc: str) -> tuple:
    re.compile(constants.PYUGIOH_XD_MATS_PATTERN).findall(card_desc)

def __get_class(card_type: str) -> Any:
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

def __init_card() -> models.BaseCard:
    with open(".example/dark_magician.json","r") as fp:
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