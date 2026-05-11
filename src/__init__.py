from pyugioh.config import Config
from pyugioh.dataman  import DataManager

config = Config()

_dataman = DataManager(
        config = config
)
_dataman.get_cards()
print("Cards: ",_dataman.card_count)