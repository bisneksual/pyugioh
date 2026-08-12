from typing import Literal
import json
from pydantic import BaseModel

class Card(BaseModel):
    id: int
    name: str
    frame: str

class MonsterCard(Card):
    pass

class SpellCard(Card):
    pass

class TrapCard(Card):
    pass


if __name__=="__main__":
    with open(".example/skill.json","r") as fp:
        card_data = json.load(fp)
    if not isinstance(card_data,dict):
        exit()
        card_data['frame'] = card_data.pop()
    card = Card.model_validate(card_data)
    print(card.model_dump())