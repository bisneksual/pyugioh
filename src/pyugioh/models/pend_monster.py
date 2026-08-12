from src.pyugioh.models.monster_card import MonsterCard

class PendulumMonster(MonsterCard):
    pend_desc: str
    scale: int

    def __init__(self, **data):
        __card_data = data
        __card_data['desc'] = __card_data.pop("monster_desc")
        super().__init__(**data)