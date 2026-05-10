import requests
import json

class DataManager:

    def __init__(self,url:str,path:str) -> None:
        print("[dataman] Initializing...")

        self._url = url
        self._data_path = path

    def get_cards(self) -> None:
        print("[dataman] Pulling YGO card data...")
        response = requests.get(self._url)
        print("[dataman] Writing response to file...")
        with open(f"{self._data_path}/ygo_cards.json","w") as fp:
            json.dump(response.json(),fp)
        print("[dataman] Done!")