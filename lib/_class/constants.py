BANLIST_MAP = ('Forbidden','Limited','Semi-Limited','Unlimited')

LINKMARKER_MAP = ('Top','Top-Right','Right','Bottom-Right','Bottom','Bottom-Left','Left','Top-Left')

DECKZONEKEYS = ('main','extra','side','skill')

SQLITE_SCHEMAS = {
    "cardlist": {
        "card_type": {"type": "text"},
        "passcode": { "type": "int", "constraints": ["primary key"]},
        "name": {"type": "text"},
        "type": {"type": "text"},
        "frametype": {"type": "text"},
        "race": {"type": "text"},
        "desc": {"type": "text"},
        "p_scale":{"type": "int"},
        "p_desc": {"type": "text"},
        "l_value": {"type": "int"},
        "atk": {"type": "int"},
        "def": {"type": "int"},
        "level": {"type": "int"},
        "attriibute": {"type": "text"},
        "archetype": {"type": "text"},
        "ygoprodeck_url": {"type": "text"},
        "l_mark_n": {"type":"boolean","default":False},
        "l_mark_nw": {"type":"boolean","default":False},
        "l_mark_w": {"type":"boolean","default":False},
        "l_mark_sw": {"type":"boolean","default":False},
        "l_mark_s": {"type":"boolean","default":False},
        "l_mark_se": {"type":"boolean","default":False},
        "l_mark_e": {"type":"boolean","default":False},
        "l_mark_ne": {"type":"boolean","default":False},
    },
    "set_map":{
        "code":{"type":"text"},
        "card_id":{"type":"int"},
        "fk":{'column':"card_id",'ref':{"table":"cardlist","column":"passcode"}},
    },
    "passcode_map":{
        "code":{"type":"int"},
        "card_id":{'type':'int'},
        "fk":{'column':"card_id",'ref':{"table":"cardlist","column":"passcode"}},

    },
    "coll_info": {
        "keyname": {"type":"text","constraints":["primary key",]},
        "name":{"type":"text","constraints":['not null']},
        "comments":{"type":"text"},
        "game":{"type":"varchar(8)"},
    },
    "coll_cards": {
        "coll_name": {"fk":{'table':'coll_info','column':'keyname'}},
        "card_set_code": {"fk":{'table':'set_map','column':'code'}},
        "card_passcode": {"fk":{'table':'passcode_map','column':'code'}},
        "quantity":{"type":"int"},
    },
    "deck_info": {
        "keyname": {"type":"text","constraints":["primary key"]},
        "name": {"type":"text","contraints":["not null"]},
        "coll_key":{"fk":{"table":"coll_info","column":"keyname"}},
        "comments": {"type":"text"},
        "game": {"type":"text","enum":["ygo"]},
    },
    "deck_cards": {
        "deck_name": {"fk":{"table":"deck_info","column":"keyname"}},
        "deck_zone": {"type":"text","enum":["main","extra","side","skill"],"constraints":["not null"]},
        "card_set_code": {"fk":{'table':'set_map','column':'code'}},
        "card_passcode": {"fk":{'table':'passcode_map','column':'code'}},
        "quantity":{"type":"int"},
    }
}

SQLITE_DATAKEYS = {
    'cardlist': ['card_type','id','name','type','frameType','race','desc','scale','pend_desc','linkval','atk','def','level','attribute','archetype','ygoprodeck_url','Top','Top-Right','Right','Bottom-Right','Bottom','Bottom-Left','Left','Top-Left'],
    'coll_info': ['keyname','name','comments','game'],
    'coll_cards': ['coll_name','card_set_code','card_passcode','quantity'],
    'deck_info': ['keyname','name','coll','comments','game'],
    "deck_cards": ['deck_name','deck_zone','card_set_code','card_passcode','quantity'],
    'set_map': ['code','id'],
    'passcode_map': ['code','id'],
}