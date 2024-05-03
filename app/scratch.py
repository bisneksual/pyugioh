import pandas as pd
import json
from os import listdir

#print(listdir("./app"))

with open('./app/example/response.json','r') as file:
    jay = json.load(file)
df = pd.DataFrame(jay['data'])
print(df['type'].unique())