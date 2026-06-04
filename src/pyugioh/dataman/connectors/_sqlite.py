import sqlite3
from itertools import chain
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

    def __query(self,**kwargs) -> list|bool:
        __sanitize = lambda _str : _str \
            .replace("\\'",'`') # override single quote escape characters
        if kwargs.get('print',False):
            print("query: ",__sanitize(kwargs.get("query","")))
        self.__cursor.execute(__sanitize(kwargs.get("query","")))
        return self.__cursor.fetchall() if kwargs.get("get",False) else (0,"Success")
    
    def __iter_query(self,**kwargs):
        #try:
            self.__cursor.executemany(kwargs.get("query"),kwargs.get("vals"))
            return self.__cursor.fetchall() if kwargs.get("get",False) else (0,"Success")
        #except Exception as e:
            

    def query(self,_query:str,return_table:bool=False,vals:list = None):
        return self.__iter_query(query=_query,get=return_table,vals=vals) if vals else self.__query(query=_query,get=return_table)

    def get_tables(self):
        return self.__query(query="select name from sqlite_master where type='table';",get=True)
    

    # 0: index
    # 1: name
    # 2: type
    # 3: not null
    # 4: default value
    # 5: primary key status
    def get_schema(self,table_name:str):
        if table_name in [x[0] for x in self.get_tables()]:
            #return self.__opts.get("schema_labels",[]).append(
            return self.__query(
                query="pragma table_info('{}');"#,
                .format(
                    table_name,
                ),
                get=True
            )
            #)
        raise KeyError(table_name)

    def create_table(self,name:str,cols:list[dict] = []):
        return self.__query(
            query="create table if not exists {} ({});"#,
            .format(
                name,
                ', '.join(
                    col.get("name","") + " " 
                    + col.get("dtype","") + " " 
                    + " ".join(col.get("constraints",""))
                    for col in cols
                )
            ),
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
                query="alter table {} add column {} {} {};"
                .format(
                    table_name,
                    col_info.get("name"),
                    col_info.get("dtype"),
                    col_info.get("constraints")
                )
            )
        raise KeyError(table_name)
        
    def add_row(self,table_name:str,row_data:dict = {}):
        if table_name in [x[0] for x in self.get_tables()]:
            return self.__query(
                query="insert into {} ({}) values ({});"
                .format(
                    table_name,
                    ','.join(repr(key) for key in row_data.keys()),
                    ','.join(repr(val) for val in row_data.values())
                )
            )
        raise KeyError(table_name)
    
    #def load_table(self,table_name:str,table_data:list):
    #    if table_name in [x[0] for x in self.get_tables()]:
    #        return self.__iter_query(
    #            query="insert into {} values (?,?);".format(table_name),
    #            vals = item
    #        )
    
    def get_count(self,table_name:str):
        if table_name in [x[0] for x in self.get_tables()]:
            return self.__query(
                query="select count(*) from {};"
                .format(table_name,),
                get=True
            )
        raise KeyError(table_name)
    
    def get_head(self,table_name:str, row_count:int = 1):
        if table_name in [x[0] for x in self.get_tables()]:
            return self.__query(
                query="select * from {} limit {};"#,
                .format(table_name,row_count,),
                get=True
            )
        raise KeyError(table_name)