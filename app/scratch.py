import pandas as pd
import json
from enums.enumtype import EnumCardType

#print(listdir("./app"))

with open('./app/example/response.json','r') as file:
    jay = json.load(file)
df = pd.DataFrame(jay['data'])
print(df.head(5))

def parse(_str:str):
    return [EnumCardType[x] for x in _str.upper().split(' ') if x in [x.name for x in (EnumCardType)]]

#print(parse("XYZ Pendulum Effect Monster"))