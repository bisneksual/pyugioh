import psycopg2
import pandas as pd
import sqlalchemy as sa

DEFAULT_PARAMS = {
    'db_name':'postgres',
    'user':'bisneksual',
    'pass':'bisneksual',
    'host':'localhost',
    'port':'5432'
}

DEFAULT_DF = pd.DataFrame([(f"string_{i}",i,(i % 2!=0)) for i in range(1,6)],columns=["Test String","Test Integer","Test Boolean"])

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
    
    def __run_query(self,query):
        if self.__connection:
            curse = self.__connection.cursor()
            try:
                curse.execute(query)
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

    def create_table(self,table_name,replace=False):
        if replace:
            self.__run_query(f"DROP TABLE IF EXISTS {table_name};")
        self.__run_query(f"CREATE TABLE IF NOT EXISTS {table_name} ();") 
    
    def create_table_from_df(self,table_name,df:pd.DataFrame):
        if self.__engine:
            try:
                df.to_sql(table_name,self.__engine)
            except Exception as e:
                print(f"Error creating table: {e}")


    def fetch_table(self,table_name):
        self.__run_query(f"SELECT * FROM {table_name};")
    
    def schema_table(self,table_name):
        self.__run_query(f"""SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
                            FROM information_schema.columns
                            WHERE table_name = '{table_name}';""")
    
    def add_column(self,table_name,col_name,dtype,constraints = None):
        self.__run_query(f"""ALTER TABLE IF EXISTS {table_name}
                             ADD COLUMN IF NOT EXISTS {col_name} {dtype} {constraints if constraints else ""};""")
    
    def remove_column(self,table_name,col_name):
        self.__run_query(f"""ALTER TABLE IF EXISTS {table_name}
                             DROP COLUMN IF EXISTS {col_name};""")
        
    def add_row(self,table_name,row_values:list):
        self.__run_query(f"""INSERT INTO {table_name}
                             VALUES ({",".join([repr(val) for val in row_values])});""")
        
    def add_rows(self,table_name,data:list[list]):
        self.__run_query(f"""INSERT INTO {table_name}
                             VALUES {",".join(["(" + ",".join([repr(val) for val in row]) + ")" for row in data])};""")
        
    def remove_table(self,table_name):
        self.__run_query(f"DROP TABLE IF EXISTS {table_name};")

    def __del__(self):
        self.__connection.close()

if __name__=="__main__":
    db = PostgresDB('postgres','bisneksual','bisneksual','localhost','5432')
    db.create_table('sample_table',replace=True)
    db.add_column('sample_table','piece','VARCHAR(255)')
    db.add_column('sample_table','is_captured','BOOLEAN')
    #for piece in ("Pawn","Knight","Bishop","Rook","Queen","King"):
    #    db.add_row('sample_table',["Pawn"])
    db.add_rows('sample_table',[["Pawn",True],["Knight",False],["Bishop",True],["Rook",False],["Queen",True],["King",False]])
    db.fetch_table('sample_table')