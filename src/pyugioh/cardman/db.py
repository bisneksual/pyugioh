from pyugioh.models.pydantic import utils
from pyugioh.models.pydantic import BaseCard
from pyugioh.cardman.tables import CardlistTable, md_obj
import json
import sqlalchemy as sa
from pathlib import Path

def init_card(path: Path,**kwargs) -> BaseCard:
    if not path.exists():
        raise FileNotFoundError
    with path.open("r") as fp:
        card_data = json.load(fp)
    if not isinstance(card_data,dict):
        raise TypeError
    card_class = utils.get_class(card_data.get("type","N/A"))
    card = card_class.model_validate(card_data)
    if "set_code" in kwargs:
        card.set_code = kwargs.get("set_code")
    return card

def load_cardlist(path: Path, engine: sa.Engine):
    CardlistTable.drop(engine,checkfirst=True)

    md_obj.create_all(engine)

    if not path.exists():
        raise FileNotFoundError
    with path.open("r") as fp:
        cardlist_data = json.load(fp)
    if not isinstance(cardlist_data,dict):
        raise TypeError
    with engine.begin() as conn:
        #i = 0
        for card in cardlist_data.get("data",[]):
            #if i>100:
            #   break
            try:
                card_class = utils.get_class(card.get("type","N/A"))
                pydantic_card = card_class.model_validate(card)
                conn.execute(CardlistTable.insert(),[pydantic_card.model_dump()])
            except Exception as e:
                print(str(card_class),": ",card)
                print(str(e))
                continue
            #i += 1
        results = conn.execute(sa.select(sa.func.count()).select_from(CardlistTable)).fetchall()

    for record in results:
        print(record)

if __name__=="__main__":
    ngin = sa.create_engine("sqlite:///db/pygo.db",echo=False)
    load_cardlist(Path("/home/bisneksual/Documents/pyugioh/data/cardlist.json"),ngin)