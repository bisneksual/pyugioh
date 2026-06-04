from pyugioh.config import Config
from pyugioh.dataman  import DataManager
import os

config_path = os.environ['PYUGIOH_CONFIG']
# print('config_path: ',config_path)

config = Config(config_path=config_path)

_dataman = DataManager(
        config = config.get("dataman")
)
_dataman.get_cards()
print(_dataman.list_cards())