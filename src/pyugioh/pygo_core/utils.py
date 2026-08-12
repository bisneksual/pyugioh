"""
Script that holds utility functions used by the Pyugioh module.
"""

import re
from src.pyugioh.pygo_core import constants

def sanitize_desc(card_desc:str) -> str:
    """
    Used to sanitize a card's description for storage in Pydantic models.

    Double apostrophes are removed from the description text of Normal Monsters to improve readability.

    :param card_desc: the description of the card
    :type card_desc: str

    :rtype: str
    :returns: the passed in string formatted for viewabililty and compatibility
    """
    return card_desc.strip("'") ## strip double quotes from normal monster descriptions

def get_pend_desc(card_desc:str) -> str:
    return re.compile(constants.PYUGIOH_PEND_DESC_PATTERN).findall(card_desc)

def get_xd_mats(card_desc: str) -> tuple:
    re.compile(constants.PYUGIOH_XD_MATS_PATTERN).findall(card_desc)