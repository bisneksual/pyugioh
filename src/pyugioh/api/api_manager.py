import requests
import json
from datetime import datetime
from pathlib import Path
import time

class APIManager:
    __query_info_keys: list = ["latest_version","last_updated","last_checked"]

    def __init__(self,config:dict):
        self.__endpoint = config.get("api_endpoint")
        self.__version_endpoint = config.get("api_version_endpoint")
        self.__data_path = Path(config.get("data_path"))
        self.__db_path = Path(config.get("db_path"))
        self.__query_path = Path(config.get("query_info_path"))

        with self.__query_path.open("r") as fp:
            self.__query_info = json.load(fp)
        
    def get_api_last_updated(self):
        response = requests.get(self.__version_endpoint)
        time.sleep(1)
        version_dict = dict(json.loads(response.text)[0])
        return version_dict

    def update(self):
        api_updated = self.get_api_last_updated()
        self.__query_info['last_checked'] = datetime.strftime(datetime.now(),"%Y-%m-%d %h:%M:%S")
        if (
            datetime.strptime(
                api_updated.get("last_update"),
                "%Y-%m-%d %h:%M:%S"
            ) - datetime.strptime(
                self.__query_info.get("last_updated","1900-01-01 00:00:00"),
                "%Y-%m-%d %h:%M:%S"
            )
        ).days > 0:
            print("It's been at least a day since the last YGOPRODECK update. Time to get a new cardlist!")
            response = requests.get(self.__endpoint)
            time.sleep(1)
            if response.status_code==200:
                self.__data_path.write_text(response.text)
                print("Card list updated!")
                self.__query_info['last_updated'] = datetime.strftime(datetime.now(),"%Y-%m-%d %h:%M:%S")
                self.__query_info['latest_version'] = api_updated.get("database_version")
        with self.__query_path.open("w") as fp:
            json.dump(self.__query_info,fp,indent=4)

if __name__=="__main__":
    pass