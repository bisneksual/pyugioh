import psycopg2
import pandas as pd
import sqlalchemy as sa
import json

DEFAULT_PARAMS = {
    'db_name':'postgres',
    'user':'bisneksual',
    'pass':'bisneksual',
    'host':'localhost',
    'port':'5432'
}

DEFAULT_DF = pd.DataFrame([(f"string_{i}",i,(i % 2!=0)) for i in range(1,6)],columns=["Test String","Test Integer","Test Boolean"])

BANLIST_MAP = ('Forbidden','Limited','Semi-Limited','Unlimited')

class PostgresDB:

    def __init__(self,dbname,uname,passw,hostname,portnum):
        try:
            self.__connection = psycopg2.connect(database=dbname,
                                        user=uname,
                                        password=passw,
                                        host=hostname,
                                        port=portnum)
            print('psycopg2: Connected.')
        except:
            print('psycopg2: Oops.')
        
        try:
            self.__engine = sa.create_engine(f"postgresql://{uname}:{passw}@{hostname}:{portnum}/{dbname}")
            print("sqlalchemy: Engine created.")
        except Exception as e:
            print(f"sqlalchemy: {e}")

    def __current_db(self):
        if self.__connection:
            return str(self.__connection.info.dbname)
    
    def __run_query(self,query,_print=False):
        if self.__connection:
            curse = self.__connection.cursor()
            try:
                curse.execute(query)
                if _print:
                    rows = curse.fetchall()
                    col_names = [desc[0] for desc in curse.description]
                    df = pd.DataFrame(rows,columns=col_names)
                    if df.shape[0]!=0:
                        print(df.head())
                    print(f"Query ran successfully, {len(rows)} rows returned.")
            except (Exception,psycopg2.DatabaseError) as e:
                print(f"Error: {e}")
            finally:
                curse.close()
                self.__connection.commit()

    def list_tables(self):
        self.__run_query("""SELECT table_name FROM information_schema.tables
                            WHERE table_schema = 'public';""")

    def create_table(self,table_name,replace=False,cascade=False):
        if replace:
            self.__run_query(f"DROP TABLE IF EXISTS {table_name} {'CASCADE' if cascade else ''};")
        self.__run_query(f"CREATE TABLE IF NOT EXISTS {table_name} ();") 
    
    def create_table_from_df(self,table_name,df:pd.DataFrame):
        if self.__engine:
            try:
                df.to_sql(table_name,self.__engine)
            except Exception as e:
                print(f"Error creating table: {e}")


    def fetch_table(self,table_name):
        self.__run_query(f"SELECT * FROM {table_name};",True)
    
    def schema_table(self,table_name):
        self.__run_query(f"""SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
                            FROM information_schema.columns
                            WHERE table_name = '{table_name}';""",True)
    
    def add_column(self,table_name,col_name,dtype,constraints = None):
        self.__run_query(f"""ALTER TABLE IF EXISTS {table_name}
                             ADD COLUMN IF NOT EXISTS {col_name} {dtype} {constraints if constraints else ""};""")
    
    def remove_column(self,table_name,col_name):
        self.__run_query(f"""ALTER TABLE IF EXISTS {table_name}
                             DROP COLUMN IF EXISTS {col_name};""")
        
    def add_row(self,table_name,row_values:tuple):
        self.__run_query(f"""INSERT INTO {table_name}
                             VALUES ({",".join([repr(val) for val in row_values])});""")
        #print(f"""INSERT INTO {table_name} VALUES ({",".join([repr(val) for val in row_values])});""")

    def add_rows(self,table_name,data:list[tuple]):
        self.__run_query(f"""INSERT INTO {table_name}
                             VALUES {",".join(["(" + ",".join([repr(val.strip("'")) for val in row]) + ")" for row in data])};""")
        
    def add_foreign_key(self,constraint_name,src_table,src_col,dest_table,dest_col,constraint_content=None):
        self.__run_query(f"""ALTER TABLE IF EXISTS {dest_table} DROP CONSTRAINT IF EXISTS {constraint_name};
                             ALTER TABLE IF EXISTS {dest_table} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({dest_col}) REFERENCES {src_table}({src_col}) {constraint_content if constraint_content else ''};""")

    def remove_table(self,table_name):
        self.__run_query(f"DROP TABLE IF EXISTS {table_name};")

    def __del__(self):
        self.__connection.close()

if __name__=="__main__":
    db = PostgresDB('postgres','bisneksual','bisneksual','localhost','5432')
    db.create_table('cardlist',replace=True,cascade=True)
    db.add_column('cardlist','PASSCODE','VARCHAR(8)','PRIMARY KEY')
    db.add_column('cardlist','CARDNAME','VARCHAR(255)')
    db.add_column('cardlist','CARDFRAME','VARCHAR(16)')
    db.add_column('cardlist','CARDDESC','VARCHAR')
    db.add_column('cardlist','CARDPDESC','VARCHAR')
    db.add_column('cardlist','CARDTYPE','VARCHAR(32)')
    db.add_column('cardlist','CARDHTYPE','VARCHAR(32)')
    db.add_column('cardlist','CARDRACE','VARCHAR(32)')
    db.add_column('cardlist','CARDATTR','VARCHAR(16)')
    db.add_column('cardlist','CARDLVL','SMALLINT')
    db.add_column('cardlist','CARDPSCALE','SMALLINT')
    db.add_column('cardlist','CARDARCH','VARCHAR(32)')
    db.add_column('cardlist','CARDATK','SMALLINT')
    db.add_column('cardlist','CARDDEF','SMALLINT')
    #db.schema_table('cardlist')

    db.create_table('setlist',replace=True)
    db.add_column('setlist','PASSCODE','VARCHAR(8)')
    db.add_column('setlist','SETCODE','VARCHAR(64)')
    db.add_column('setlist','NAME','VARCHAR(255)')
    db.add_column('setlist','RARITY','VARCHAR(8)')
    db.add_column('setlist','PRICE','REAL')
    db.add_foreign_key('fk_card','cardlist','PASSCODE','setlist','PASSCODE','ON DELETE CASCADE')

    db.create_table('pricelist',replace=True)
    db.add_column('pricelist','PASSCODE','VARCHAR(8)')
    db.add_column('pricelist','MARKET','VARCHAR(31)')
    db.add_column('pricelist','CARDPRICE','REAL')
    db.add_foreign_key('fk_card','cardlist','PASSCODE','pricelist','PASSCODE','ON DELETE CASCADE')

    db.create_table('banlist',replace=True)
    db.add_column('banlist','PASSCODE','VARCHAR(8)')
    db.add_column('banlist','RULESET','VARCHAR(5)')
    db.add_column('banlist','BANLIMIT','SMALLINT')
    db.add_foreign_key('fk_card','cardlist','PASSCODE','banlist','PASSCODE','ON DELETE CASCADE')

    fp = open('/home/bisneksual/Documents/GitHub/pyugioh/db/sample/sample_card_pendulum.json','r')
    card = json.load(fp)
    card_data = card['data'][0]

    db.add_row('cardlist',(
                            card_data.get('id'), #PASSCODE
                            card_data.get('name','~NONAME~'), #CARDNAME
                            card_data.get('frameType','~NOFRAME~'), #CARDFRAME
                            card_data['monster_desc'] if 'monster_desc' in card_data else card_data.get('desc','~NODESC~').strip("'"), #CARDDESC
                            card_data.get('pend_desc',"~NOPDESC~"), #CARDPDESC
                            card_data.get('type','~NOTYPE~'), #CARDTYPE
                            card_data.get('humanReadableCardType','~NOHTYPE~'), #CARDHTYPE)
                            card_data.get('race','~NORACE~'), #CARDRACE
                            card_data.get('attribute','~NOATTR~'), #CARDATTR
                            card_data.get('level',0), #CARDLVL
                            card_data.get('scale',0), #CARDPSCALE
                            card_data.get('archetype','~NOAfRCH~'), #CARDARCH
                            card_data.get('atk',0), #CARDATK
                            card_data.get('def',0) #CARDDEF
                           )
    )
    db.fetch_table('cardlist')

    for card_set in card_data.get('card_sets',[]):
        db.add_row('setlist',(
                                card_data['id'], #PASSCODE
                                card_set['set_code'], #SETCODE
                                card_set['set_name'].replace("'","`"), #NAME
                                card_set['set_rarity_code'], #RARITY
                                card_set['set_price'] #PRICE
                             )
        )
    db.fetch_table('setlist')
    
    #print(type(card_data['card_prices']))
    if 'card_prices' in card_data:
        for k, v in card_data['card_prices'][0].items():
            db.add_row('pricelist',(
                                    card_data['id'], #PASSCODE
                                    k.split('_')[0] if "_" in k else k, #MARKET
                                    v #CARDPRICE
                                   )
            )
    db.fetch_table('pricelist')
    
    if 'banlist_info' in card_data:
        for rule, limit in card_data['banlist_info'].items():
            try:
                db.add_row('banlist',(
                                        card_data['id'], #PASSCODE
                                        rule.split('_')[-1], #RULESET
                                        BANLIST_MAP.index(limit) #BANLIMIT
                                     )
                )
            except ValueError as ve:
                continue
    db.fetch_table('banlist')

    fp.close()
