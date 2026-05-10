from pyugioh.config import config
from pyugioh.dataman  import DataManager

#def main() -> int:
#_config = PyugiohConfig()
#print(_config.config.sections())
_dataman = DataManager(
        url=config.get("dataman").get("api_url",""),
        path=config.get("dataman").get("data_path","")
)
_dataman.get_cards()
print("Hello!")
#return 0