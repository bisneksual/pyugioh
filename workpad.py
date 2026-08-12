import json
import pandas as pd

schema = {
    "card_set_code":{"type":"text"},
    "quantity":{"type":"int"},
    "(fk)": [
        {"coll_name":{'table':'coll_info','column':'keyname'}},
        {"card_set_code":{'table':'set_map','column':'code'}},
        {"card_passcode":{'table':'passcode_map','column':'code'}}
    ]
}

query = ','.join(
    ','.join(
            'foreign key (' + next(iter(row.keys())) + ") references " + next(iter(row.values())).get('table') + "(" + next(iter(row.values())).get('column') + ")"
         for row in val1) if key1=='(fk)'
        else (key1 + " " + val1.get('type'))
    for key1,val1 in schema.items() #tables
)
print(query)