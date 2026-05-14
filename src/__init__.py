from pyugioh.config import Config
from pyugioh.dataman  import DataManager
import os

config_path = os.environ['PYUGIOH_CONFIG']

config = Config()

_dataman = DataManager(
        config = config
)
_dataman.get_cards()
print("Cards: ",_dataman.card_count)

print(_dataman.tables())