import sqlite3
from pyugioh.dataman.connectors.base_connector import _Connector

class SQLite3Connector(_Connector):
    def __init__(self,**kwargs):
        super().__init__()

        args = kwargs.get('config',{})
        self.__opts = args.get("sqlite3",{})
        self.__db = args.get("db_path","vol/data/pyugioh.db")
        self.__conn = None
        self.__cursor = None
    
    def connect(self) -> None:
        try:
            self.__conn = self.__connect(self.__db)
            self.__cursor = self.__conn.cursor()
            self.__conn.row_factory = sqlite3.Row
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
            return self.__cursor.fetchall() if kwargs.get("get",False) else (0,"Success")
        except Exception as e:
            return 1, str(e)
    
    def query(self,_query:str,return_table:bool=False):
        return super().query(query=_query,get=return_table)

    def get_tables(self):
        return self.__query(query="select name from sqlite_master where type='table';",get=True)
    

    # 0: index
    # 1: name
    # 2: type
    # 3: not null
    # 4: default value
    # 5: primary key status
    def get_schema(self,name):
        if name in [x[0] for x in self.get_tables()]:
            return self.__opts.get("schema_labels",[]).append(
                self.__query(
                    query="pragma table_info('{}');"
                    .format(
                        name
                    ),
                    get=True
                )
            )

    def create_table(self,name:str):
        return self.__query(
            query="create table if not exists {} (id integer primary key);"
            .format(
                name
            )
        )
    
    def drop_table(self,name:str):
        return self.__query(
            query="drop table if exists {};"
            .format(
                name
            )
        )
    
    def add_column(self,table_name:str,col_info:dict):
        if table_name in [x[0] for x in self.get_tables()]:
            return self.__query(
                query="alter table {} add column {} {}"
                .format(
                    table_name,
                    col_info.get("name"),
                    col_info.get("dtype")
                )
            )
