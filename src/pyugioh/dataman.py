import requests
import json

class DataManager:

    def __init__(self,config:dict) -> None:
        self._url = config.get("api",{}).get("url")
        self._data_path = config.get("data",{}).get("path")

    def get_cards(self) -> None:
        if not any((self._url,self._data_path)):
            print(",".join(key + ", " + val for key, val in dict(url=self._url,data_path=self._data_path).items()))

        response = requests.get(self._url)

        with open("cards.json","w") as fp:
            json.dump(response.json(),fp)