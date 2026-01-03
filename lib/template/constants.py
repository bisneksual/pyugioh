BANLIST_MAP = ('Forbidden','Limited','Semi-Limited','Unlimited')

LINKMARKER_MAP = ('Top','Top-Right','Right','Bottom-Right','Bottom','Bottom-Left','Left','Top-Left')

DECKZONEKEYS = ('main','extra','side','skill')

SQLITE_SCHEMAS = {
    "ygo_cardlist": {
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
    "ygo_set_map":{
        "code":{"type":"text"},
        "card_id":{"type":"int"},
        "(fk)":[
            {"card_id":{"table":"ygo_cardlist","column":"passcode"}},
        ],
    },
    "ygo_passcode_map":{
        "code":{"type":"int"},
        "card_id":{'type':'int'},
        "(fk)":[
            {"card_id":{"table":"ygo_cardlist","column":"passcode"}},
        ],
    },
    "coll_info": {
        "keyname": {"type":"text","constraints":["primary key",]},
        "name":{"type":"text","constraints":['not null']},
        "comments":{"type":"text"},
        "game":{"type":"text","enum":["ygo"]},
    },
    "ygo_coll_cards": {
        "card_set_code":{"type":"text"},
        "quantity":{"type":"int"},
        "coll_name":{"type":"text"},
        "card_set_code":{"type":"text"},
        "card_passcode":{"type":"int"},
        "(fk)": [
            {"coll_name":{'table':'coll_info','column':'keyname'}},
            {"card_set_code":{'table':'ygo_set_map','column':'code'}},
            {"card_passcode":{'table':'ygo_passcode_map','column':'code'}},
        ],
    },
    "deck_info": {
        "keyname": {"type":"text","constraints":["primary key"]},
        "name": {"type":"text","contraints":["not null"]},
        "coll_key":{"type":"text"},
        "comments": {"type":"text"},
        "game": {"type":"text","enum":["ygo"]},
        "(fk)":[
            {"coll_key":{"table":"coll_info","column":"keyname"}},
        ],
    },
    "ygo_deck_cards": {
        "deck_name": {"type":"text"},
        "deck_zone": {"type":"text","enum":["main","extra","side","skill"],"constraints":["not null"]},
        "card_set_code": {"type":"text"},
        "card_passcode": {"type":"int"},
        "quantity":{"type":"int"},
        "(fk)":[
            {"deck_name":{"table":"deck_info","column":"keyname"}},
            {"card_set_code":{'table':'ygo_set_map','column':'code'}},
            {"card_passcode":{'table':'ygo_passcode_map','column':'code'}},
        ],
    },
    "ygo_card_prices": {
        "id":{"type":"int"},
        "cardmarket":{"type":"real"},
        "tcgplayer":{"type":"real"},
        "ebay":{"type":"real"},
        "amazon":{"type":"real"},
        "coolstuffinc":{"type":"real"},
        "(fk)":[
            {"id":{"table":"ygo_cardlist","column":"passcode"}},
        ],
    },
}

SQLITE_DATAKEYS = {
    'ygo_cardlist': ['card_type','id','name','type','frameType','race','desc','scale','pend_desc','linkval','atk','def','level','attribute','archetype','ygoprodeck_url','Top','Top-Right','Right','Bottom-Right','Bottom','Bottom-Left','Left','Top-Left'],
    'coll_info': ['keyname','name','comments','game'],
    'ygo_coll_cards': ['coll_name','card_set_code','card_passcode','quantity'],
    'deck_info': ['keyname','name','coll','comments','game'],
    "ygo_deck_cards": ['deck_name','deck_zone','card_set_code','card_passcode','quantity'],
    'ygo_set_map': ['code','id'],
    'ygo_passcode_map': ['code','id'],
    "ygo_card_prices": ['id','cardmarket_price','tcgplayer_price','ebay_price','amazon_price','coolstuffinc_price'],
}