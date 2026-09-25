from pyugioh.models.pydantic import utils
from pyugioh.models.pydantic import BaseCard
from pyugioh.models.sql_alchemy.tables import CardlistTable
import json
import sqlalchemy as sa


# Will likely be implemented in the card manager
def init_card(path: str,**kwargs) -> BaseCard:
    with open(path,"r") as fp:
        card_data = json.load(fp)
    if not isinstance(card_data,dict):
        exit()
    card_class = utils.get_class(card_data.get("type","N/A"))
    card = card_class.model_validate(card_data)
    if "set_code" in kwargs:
        card.set_code = kwargs.get("set_code")
    #card_sets = {card_data.get("id"):card_data.get("card_sets")}
    #print(card_sets)
    return card

def pygo_config():
    with open(".config/config.json") as fp:
        config_dict = json.load(fp)
    if not isinstance((config_dict,dict)):
        raise TypeError("contents of config.json is not castable as dict :(")
    dataman_config = config_dict.get("dataman")

def sqlite():
    card = init_card(".example/dark_magician.json",set_code = "SDY-006")

    ngin = sa.create_engine("sqlite:///db/pygo.db",echo=True)
    md_obj = sa.MetaData()

    sa.inspect(ngin).get_table_names()

    CardlistTable.drop(ngin)

    md_obj.create_all(ngin)

    query = sa.select(CardlistTable)

    with ngin.begin() as conn:
        conn.execute(CardlistTable.insert(),[card.model_dump()])
        results = conn.execute(query).fetchall()
        for record in results:
           print(record)

if __name__=="__main__":
    sqlite()