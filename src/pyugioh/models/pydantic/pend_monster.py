from .monster_card import MonsterCard
from typing import Optional

class PendulumMonster(MonsterCard):
    pend_desc: Optional[str] = None
    scale: int

    def __init__(self, **data):
        __card_data = data
        if "monster_desc" in __card_data:
            __card_data['desc'] = __card_data.pop("monster_desc")
        super().__init__(**data)