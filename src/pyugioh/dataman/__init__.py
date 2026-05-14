import requests
import json
from pyugioh.config import Config
from pyugioh.dataman.connectors import SQLite3Connector
import pandas as pd

class DataManager:
    #DataManager (shortened to dataman)
    #Handles all disk and API operations within Pyugioh, including pulling
    # and saving new cardlist data and reading and writing files for other
    # managers
    def __init__(self,config:Config) -> None:
        #DataManager constructor.
        #:param config: Config class. Used to initialize properties.
        print("[dataman] Initializing...")

        self.config = config
        self.connect()
        self.card_count = 0

    def connect(self) -> None:
            #self.__conn = sqlite3.connect(self.config['dataman'].get("db_path"))
            self.__connector = SQLite3Connector()
            self.__connector.connect()
    
    def ping(self) -> str:
        return "pong" if isinstance(self.__connector,SQLite3Connector) and self.__connector.is_connected() else "Nope."

    def tables(self):
        return self.__connector.get_tables()

    def get_cards(self):
        #Queries API endpoint and saves full cardlist for ingestion into
        # database.
        print("[dataman] Pulling YGO card data...")
        response = requests.get(self.config['dataman'].get('api_url'))
        status = response.status_code
        cards = response.json()
        print("[dataman] Writing response to file...")
        with open(f"{self.config['dataman'].get('data_path')}/ygo_cards.json","w") as fp:
            json.dump(cards,fp)

        print("[dataman] Loading cardlist into database...")
        
        self.__load_cards(cards.get('data',[]))
        
        print("[dataman] Setting card count...")
        self.card_count = len(cards.get("data",[]))

        print("[dataman] Done!")
    
    #def query(self,query:str):
    #    if self.__connected():
    #        try:
    #            curse = self.__conn.cursor()

    def __load_cards(self,cardlist:list[dict]) -> None:
        #Takes in a cardlist in dictionary format, cleans the data types,
        # and loads the data into a selected database (default: sqlite)
        df_cards = pd.DataFrame(cardlist)
        df_codes = df_cards.explode('card_sets')
        #print(df_codes.head())
        

        print("[dataman] Printing schema...")
        df_cards.info()
