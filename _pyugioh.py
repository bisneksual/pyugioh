import re
import os
from pathlib import Path
from configparser import ConfigParser
import json
import yaml
import pandas as pd
import sqlite3
from lib.template.constants import SQLITE_SCHEMAS, SQLITE_DATAKEYS

from lib.ygo import YGOCardList

class APIManager:

    def __init__(self):
        pass

class DataManager:
    def __connect(self,name:str):
        try:
            self.__db = sqlite3.connect(name)
            self.__cursor = self.__db.cursor()
            return 0 #successful connection
        except sqlite3.Error as e:
            print("[connect] {}".format(e))
            return 1 #unsuccessful connection
        
    def __conn_exists(self):
        return not (self.__db is None or self.__cursor is None)

    def table_exists(self,table:str = None):
        if table and self.__conn_exists():
            result = self.do("SELECT name FROM sqlite_master WHERE type='table' and name='{}';".format(table),True)
            return (len(result)==1)

    def __do(self,query:str,get_result:bool=False,quiet:bool=False):
        if not self.__conn_exists():
            return 2 #problem with db connection
        if not query:
            return 1 #no query passed in
        try:
            self.__cursor.execute(query)
            _result = self.__cursor.fetchall()
            return _result if get_result and _result is not None else 0
        except sqlite3.Error as e:
            if not quiet:
                print("[__do] {} => {}".format(query,e))
            return 9 #sql error
    def __remove_entry(self,table:str,row_id:int):
        pass
    
    def __init_schemas(self,schemas:dict[str:dict]):
        self.__schemas = {
            t_key:','.join(
                (
                    ','.join(
                        'foreign key (' + next(iter(row.keys())) + ") references " + next(iter(row.values())).get('table') + "(" + next(iter(row.values())).get('column') + ")"
                        for row in val
                    ) if key=='(fk)' else 
                    (
                        key + " " + \
                        (val['type'] if 'type' in val else '') + " " +\
                        (' '.join(val['constraints'] if 'constraints' in val else list())) + " " + \
                        ("default " + str(val.get('default')) if 'default' in val else '') + " " + \
                        (('check (' + key + ' in (' + ','.join(repr(x) for x in val.get(('enum'))) + '))') if 'enum' in val else '')
                    )
                ) for key, val in table.items()
            ) for t_key,table in schemas.items()
        }

    def __init__(self,db_name:str):
        self.db_name = db_name
        result = self.__connect(db_name)
        print('[__connect] {}'.format(result))

        self.__init_schemas(SQLITE_SCHEMAS)

    def get_schema(self,table:str):
        return self.__schemas.get(table,"Table {} not found".format(table))

    def do(self,query:str,result:bool=False):
        return self.__do(query,result)
    
    def create_table(self,table:str):
        if table not in self.__schemas.keys():
            return 2 #table not found
        if not self.__conn_exists():
            return 3 #problem with database connection
        try:
            self.__do("DROP TABLE IF EXISTS {};".format(table))
            self.__do("CREATE TABLE {} ({});".format(table,self.__schemas[table]))
            return 0 #successful creation
        except sqlite3.Error as e:
            print("[create table] {}".format(e))
            return 9 #sql error
        
    def get_table(self,table:str):
        if table not in self.__schemas.keys():
            return 2 #table not found in schema
        if not self.__conn_exists():
            return 3 #problem with database connection
        if not self.table_exists(table):
            return 4 #table not defined yet
        try:
            df = pd.read_sql_query("SELECT * FROM {}".format(table),self.__db)
            return df
        except sqlite3.Error as e:
            print("[get table] {}".format(e))
            return 9 #sqlite error
        
    def add_entry(self,table:str,data:dict):
        if table not in self.__schemas.keys():
            return 2 #table not found
        if not self.__conn_exists():
            return 3 #problem with database connection
        keys = SQLITE_DATAKEYS[table]
        entry = [repr('NULL' if data.get(x,"NULL") is None else data.get(x,'NULL')) for x in keys]
        try:
            result = self.__do("INSERT INTO {} VALUES ({});".format(table,','.join(entry)),quiet=False)
            return result #successful addition
        except sqlite3.Error as e:
            print('[add entry] {}'.format(e))
            return 9 #sqlite error
    
    def remove_entry(self,table:str,**kwargs):
        print(kwargs)

    def __del__(self):
        self.__db.close()

class PyugiohConfig:

    def __init__(self):
        self.__home_path = Path(__file__).parent.parent

        #print(self.__home_path)
        self.__config_path = os.path.join('config/pyugioh.ini')

        if os.path.isfile(self.__config_path):
            cparse = ConfigParser()
            cparse.read(self.__config_path)
            #print(cparse.sections())
            
            self.api_path = os.path.join(self.__home_path,cparse.get('ygo','api_path'))
            self.deck_path = os.path.join(self.__home_path,cparse.get('ygo','deck_path'))
            self.coll_path = os.path.join(self.__home_path,cparse.get('ygo','coll_path'))
            self.db_name = cparse.get('ygo','db_name') + '.db'
        else:
            print('Oops. Config file not found.')

class Pyugioh:
    
    def __init_deckman(self):
        path = self.config.deck_path
        #self.deckman = ygo.YGODeckManager(path)
        pass

    def __init_dataman(self):
        db = self.config.db_name
        self.dataman = DataManager(db)
        pass

    def __init_apiman(self):
        path = self.config.api_path
        #self.apiman = APIManager()

    def __init_collman(self):
        _path = self.config.coll_path
        #self.collman = ygo.YGOCollectionManager(_path)
    
    #def __data_load()

    def __init__(self):
        self.config = PyugiohConfig()
        #self.validator = ygo.YGOValidator()
        
        self.__init_dataman()
        self.__init_deckman()
        self.__init_collman()
        self.__init_apiman()

if __name__=="__main__":
    #sys.path.append("~/Documents/pyugioh")

    pygo = Pyugioh()
    result = pygo.dataman.get_schema('coll_cards')
    print(result)