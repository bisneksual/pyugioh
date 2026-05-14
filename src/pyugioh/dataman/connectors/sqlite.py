import sqlite3
from pyugioh.dataman.connectors.base_connector import _Connector

class SQLite3Connector(_Connector):
    def __init__(self,**kwargs):
        super().__init__()

        args = kwargs
        self.__db = args.get("db","vol/data/pyugioh.db")
        self.__conn = None
        self.__cursor = None
    
    def connect(self) -> None:
        try:
            self.__conn = self.__connect(self.__db)
            self.__cursor = self.__conn.cursor()
        except Exception as e:
            print(str(e))
    
    def is_connected(self) -> bool:
        try:
            return (self.__conn.cursor() is not None)
        except:
            return False
        
    def __connect(self,db: str) -> sqlite3.Connection:
        return sqlite3.connect(self.__db)

    def __query(self,**kwargs) -> list|tuple[int,str]:
        try:
            self.__cursor.execute(kwargs.get("query"))
            return self.__cursor.fetchall() if kwargs.get("get") else (0,"Success")
        except Exception as e:
            return 1, str(e)
    
    def query(self,_query:str,return_table:bool=False):
        return super().query(query=_query,get=return_table)

    def get_tables(self):
        return self.__query(query="select name from sqlite_master where type='table';",get=True)