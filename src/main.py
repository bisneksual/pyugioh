from src.pyugioh.pygo_core import utils
from src.pyugioh.models import BaseCard
import json


# Will likely be implemented in the card manager
def init_card(path: str) -> BaseCard:
    with open(path,"r") as fp:
        card_data = json.load(fp)
    if not isinstance(card_data,dict):
        exit()
    card_class = utils.get_class(card_data.get("type","N/A"))
    card = card_class.model_validate(card_data)
    return card

if __name__=="__main__":
    card = init_card(".example/dark_magician.json")
    print(type(card))
    print(card.model_dump())