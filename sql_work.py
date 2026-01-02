import sqlite3
import pandas as pd
import json
import yaml
from lib.constants import SQLITE_SCHEMAS, SQLITE_DATAKEYS

class DataManager:
    def __connect(self):
        try:
            self.__db = sqlite3.connect("pyugioh.db")
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
    
    def __init_schemas(self,schemas:dict[str:dict]):
        self.__schemas = {t_key:','.join(
            "{} {} {} {} {} {} {} {}".format(
                "foreign key (" if key=='fk' else "",
                val.get('column') if key=='fk' else key,
                ")" if key=='fk' else "",
                val['type'] if 'type' in val else "",
                ('references ' + val.get('ref').get('table') + '(' + val.get('ref').get('column') + ')') if key=='fk' else "",
                ' '.join(val['constraints'] if 'constraints' in val else list()),
                "default " + str(val.get('default')) if 'default' in val else '',
                ("check (" + key + " in (" + ','.join(repr(x) for x in val.get(('enum'))) + "))") if 'enum' in val else ''
            ) for key, val in table.items()
        ) for t_key,table in schemas.items()}

    def __del__(self):
        self.__db.close()

    def __init__(self):
        result = self.__connect()
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

if False:
    __schemas = {t_key:','.join(
                "{} {} {} {} {} {}".format(
                    "foreign key (" if key=='fk' else "",
                    val.get('column') if key=='fk' else key,
                    ")" if key=='fk' else "",
                    val['type'] if 'type' in val else "",
                    ('references ' + val.get('ref').get('table') + '(' + val.get('ref').get('column') + ')') if key=='fk' else "",
                    ' '.join(val['constraints'] if 'constraints' in val else list()),
                    "default " + str(val.get('default')) if 'default' in val else ''
                ) for key, val in table.items()
            ) for t_key,table in SQLITE_SCHEMAS.items()}

    print(__schemas['set_map'])

dataman = DataManager()

#exit()

# Build cardlist table with data on each card 

print('[create table] {}'.format(dataman.create_table('cardlist')))

with open('example/all.json','r') as fp:
    all_cards = json.load(fp)

card_data = all_cards.get('data')

# Build set code map dictionary for loading later

_set_map = {card.get('id'):[x.get('set_code') for x in card.get('card_sets',())] for card in card_data}

# Build passcode map dictionary for loading later

_passcode_map = {card.get('id'):[x.get('id') for x in card.get('card_images',[])] for card in card_data}

#Iterate through each card entry in the API response

for card in card_data:
    #Assign the card supertype to the card based on the contents of the card type attribute

    _type = card.get('type')
    card['card_type'] =         'extra' if any(x in _type for x in ('Link','Fusion','Syncro','XYZ')) \
                        else    'skill' if "Skill" in _type \
                        else    'spell' if 'Spell' in _type \
                        else    'trap' if "Trap" in _type \
                        else    'token' if "Token" in _type \
                        else    'monster' if "Monster" in _type \
                        else    'NULL'

    #Separate the monster and pendulum descriptions in the case of a pendulum monster

    card['desc'] =  card.get('monster_desc',card.get('desc'))

    #Clean apostrophes and single quoted out of the monster and pendulum descriptions for parsing purposes

    card['desc'] =  card['desc'] \
                    .replace("\'","`")
    
    if 'pend_desc' in card:
        card['pend_desc'] = card['pend_desc'] \
                            .replace("\'","`")

    #Pass the card into to the data manager to be added to the cardlist table

    dataman.add_entry('cardlist',card)

#Fetch the contents of the cardlist table to verify that all of the API response entries were parsed and none were rejected
df = dataman.get_table('cardlist')
print(len(df))

#Create a table in the pyugioh database specifically for the set code map

print('[create table] {}'.format(dataman.create_table('set_map')))

#Iterate through the dictionary items and parse the value pairs into the SQL table

for card,codes in _set_map.items():
    for code in codes:
        dataman.add_entry('set_map',{'id':card,'code':code})

#Fetch the set map table to verify that the data was parsed correctly
df = dataman.get_table('set_map')
print(df.head())

#Create a table in the pyugioh database specifically for the passcode map

print('[create table] {}'.format(dataman.create_table('passcode_map')))

#Iterate through the passcode map and parse each value pair into the SQL table

for card,codes in _passcode_map.items():
    for code in codes:
        dataman.add_entry('passcode_map',{'id':card,'code':code})

#Fetch the passcode map table to verify that the data was parsed correctly
df = dataman.get_table('passcode_map')
print(len(df))

print('[create table] {}'.format(dataman.create_table('coll_info')))

with open("colls/e8f6a076-3ac4-4396-a3f2-6371814f73a0.coll","r") as fp:
    coll = yaml.safe_load(fp)

coll_data = coll.get('coll')

print('[add entry] {}'.format(dataman.add_entry('coll_info',coll_data)))

df = dataman.get_table('coll_info')
print(df.head())

print('[create table] {}'.format(dataman.create_table('coll_cards')))

key = coll_data.get('keyname')
cards = coll_data.get('cards')

for card in cards:
    code, quantity = next(iter(card.items())) if isinstance(card,dict) else (card,1)
    row = {'coll_name':key,'card_set_code':(code if isinstance(code,str) else None),'card_passcode':code if isinstance(code,int) else None,'quantity':quantity}
    print('[add entry] {}'.format(dataman.add_entry('coll_cards',row)))

df = dataman.get_table('coll_cards')
print(df.head())

with open("decks/675be712-4201-4cb2-a862-2e035901e241.deck","r") as fp:
    deck = yaml.safe_load(fp)

deck_data = deck.get('deck')

print('[create table] {}'.format(dataman.create_table("deck_info")))

print("[add entry] {}".format(dataman.add_entry("deck_info",deck_data)))

df = dataman.get_table('deck_info')
print(df.head())

print('[create table] {}'.format(dataman.create_table('deck_cards')))

key = deck_data.get('keyname')
deck_cards = deck_data.get('cards')

for zone, cards in deck_cards.items():
    for card in cards:
        code, quantity = next(iter(card.items())) if isinstance(card,dict) else (card,1)
        row = {'deck_name':key,'deck_zone':zone,'card_set_code':(code if isinstance(code,str) else None),'card_passcode':code if isinstance(code,int) else None,'quantity':quantity}
        print('[add entry] {}'.format(dataman.add_entry('deck_cards',row)))

df = dataman.get_table('deck_cards')
print(df.head())