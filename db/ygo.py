import json
from constants import BANLIST_MAP,LINKMARKER_MAP
import re
from class_pyugioh import Card

class YGOCard(Card):
    
    def __init__(self, data_card: dict,**kwargs):
        super().__init__(data_card)
        self.game = 'ygo'
        self.__images = self.get_data().get('card_images')

        _data = self.get_data()
        self.desc = _data.get('desc').replace("''","").replace('\u25cf','>')
        self.race = _data.get('race')
        self.hasArchetype = ('archetype' in _data)

        if self.hasArchetype:
            self.archetype = _data.get('archetype')
        _prices = _data.get('card_prices')[0]

        if _prices:
            for shop in _prices:
                _prices[shop] = float(_prices[shop])
        self.prices = _prices

        _codes = _data.get('card_images')
        _code_list = [x.get('id') for x in _codes if isinstance(x,dict) and 'id' in x]
        self.passcode_list = _code_list
        self.passcode = _data.get('id')

        if 'card_sets' in _data:
            _sets = _data.get('card_sets')
            _sets_dict = {
                _set.get('set_code'): {
                    'prefix': _set.get('set_code').split('-')[0],
                    'name': _set.get('set_name'),
                    'ratity':  _set.get('set_rarity'),
                    'price': _set.get('set_price')
                } for _set in _sets
            }
            self.sets = _sets_dict

        self.urlTag = _data.get('ygoprodeck_url').split('/')[-1]


        _ban = _data.get('banlist_info')
        if _ban:
            _ban_map = {key.split('_')[-1]: BANLIST_MAP.index(_ban[key]) for key in _ban}
            self.banlist = _ban_map

        if 'passcode' in kwargs:
            self.secondaryPasscode = kwargs.get('passcode')
        
        if 'set_code' in kwargs:
            self.secondarySetCode = kwargs.get('set_code')

        del _data
    
    #Overriden method that returns a printout of important card information
    #Specifically, this will remove the inherited card data dict as well as the urls for card images
    def __repr__(self):
        vars = self.__dict__
        for key in ('_Card__data','_YGOCard__images','sets','prices'):
            if key in vars:
                del vars[key]

        return repr(vars)
    
    #Pretty prints the card data using the repr method
    def pp(self):
        info = repr(self)
        return 

class YGOMonster(YGOCard):

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = 'monster'
        self.name = _data.get('name')
        self.frame = _data.get('frameType')
        self.types = _data.get('typeline')
        self.level = _data.get('level')
        self.attack = _data.get('atk')
        _def = _data.get('def')
        self.defense = _def if _def else 0
        self.attribute = _data.get('attribute')
        self.isPendulum = ('Pendulum' in _data.get('type'))

        if self.isPendulum:
            self.pScale = _data.get('scale')
            self.pDesc = _data.get('pend_desc')
            self.desc = _data.get('monster_desc').replace("''","")

        self.isTuner = ('Tuner' in _data.get('type'))
        
        self.isRitual = ("Ritual" in _data.get('type'))
        if self.isRitual:
            _desc = self.desc
            _findritual = re.findall(r'Ritual Summon(?:ed)? (?:this card )?with .*"(.*?)"(?: Ritual Spell Card)?\.',_desc)
            self.rSummon = _findritual[0] if len(_findritual)>0 else ""

        self.isGemini = ('Gemini' in _data.get('type'))
        self.isUnion = ('Union' in _data.get('type'))
        self.isToon = ('Toon' in _data.get('type'))

        del _data

class YGOSpell(YGOCard):

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = 'spell'
        self.mType= _data.get('race')

        del _data

class YGOTrap(YGOCard):

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = 'trap'
        self.tType= _data.get('race')

        del _data

class YGOToken(YGOCard):
    
    def __init__(self, data_card,secondary_code = None):
        super().__init__(data_card,secondary_code)

        self.cardType = "token"

class YGOExtraDeck(YGOMonster):

    def __init__(self,data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = "x_monster"

        if "Fusion" in _data.get('type'):
            self.xType = 'Fusion'
            
            desc_split = self.desc.split('\r\n')
            self.fCriteria = desc_split[0]
            self.desc = "" if len(desc_split) < 2 else "\r\n".join(desc_split[1:])
        
        elif "Synchro" in _data.get('type'):
            self.xType = "Synchro"
            
            desc_split = self.desc.split('\r\n')
            self.sCriteria = desc_split[0]
            self.desc = "" if len(desc_split) < 2 else "\r\n".join(desc_split[1:])

        elif "Link" in _data.get('type'):
            self.xType= "Link"

            desc_split = self.desc.split('\r\n')
            self.lCriteria = desc_split[0]
            self.desc = "" if len(desc_split) < 2 else "\r\n".join(desc_split[1:])
            
            self.lVal = _data.get('linkval')

            _link = _data.get('linkmarkers')
            self.lMarkers = [x in _link for x in LINKMARKER_MAP]
        
        elif 'XYZ' in _data.get('type'):
            self.xType= "Xyz"

            desc_split = self.desc.split('\n')
            self.zCriteria = desc_split[0]
            self.desc = "" if len(desc_split) < 2 else "\n".join(desc_split[1:]).replace('\u25cf','\t>')
        
        del _data

class __YGOCardList:

    def __list_load(self,data:list[dict]):
        self.__card_list = data
        print('[__list_load] List loaded!')

        _codes = {
            str(y.get('id')): [
                x.get('id') for x in y.get('card_images') if isinstance(x,dict) and 'id' in x
            ] for y in data if isinstance(y,dict) and 'id' in y and 'card_images' in y
        }
        self.__passcodemap = _codes
        print('[__list_load] passcode lookup map updated!')

        _codes = {
            str(y.get('id')): [
                x.get('set_code') for x in y.get('card_sets') if isinstance(x,dict) and 'set_code' in x
            ] for y in data if isinstance(y,dict) and 'id' in y and 'card_sets' in y
        }
        self.__setcodemap = _codes
        print('[__list_load] set code lookup map updated!')

    def __search_passcodes(self,passcode:str|int):
        if isinstance(passcode,str):
            if not passcode.isnumeric():
                print(f'[__search_passcodes] Oops: invalid passcode {passcode} entered.')
                return None
        if self.__passcodemap:
            __boolmap = {key:(self.__passcodemap.get(key) and passcode in self.__passcodemap.get(key)) for key in self.__passcodemap}
            if not any(__boolmap.values()):
                print(f'[__search_passcodes] Oops: Passcode {passcode} not found')
                return None
            result = next((key for key in __boolmap if __boolmap[key]))
            return result
    
    def __search_set_codes(self,set_code:str):
        __boolmap = {key:(self.__setcodemap.get(key) and set_code in self.__setcodemap.get(key)) for key in self.__passcodemap}
        if not any(__boolmap.values()):
            print(f'[__search_set_codes] Oops: Passcode {set_code} not found')
            return None
        result = next((key for key in __boolmap if __boolmap[key]))
        return result
    
    def __get_card_data(self,passcode:str|int):
        __passcode = passcode if isinstance(passcode,int) else int(passcode) if passcode.isnumeric() else None
        if __passcode:
            _card_data = next((card for card in self.__card_list if card['id']==__passcode))
            if _card_data:
                return _card_data
            print('[__get_card_data] Oops: There was an error trying to find card data')
            return None
        #print(f'Oops: Invalid 
        print(f'[__get_card_data] Oops: Invalid passcode {passcode}')
        return None
    
    def __get_card(self,code:int,**kwargs):

        card_stuff = self.__get_card_data(code)
        if card_stuff:
            card_type = card_stuff.get('type')
            card =  YGOExtraDeck(card_stuff,**kwargs) if any((x in card_type for x in ('Fusion','Synchro','Link','XYZ'))) \
                        else YGOSpell(card_stuff,**kwargs) if 'Spell' in card_type \
                        else YGOTrap(card_stuff,**kwargs) if 'Trap' in card_type \
                        else YGOToken(card_stuff,**kwargs) if 'Token' in card_type \
                        else YGOMonster(card_stuff,**kwargs) if 'Monster' in card_type \
                        else None
            if card:
                return card
            print('[from_passcode] Oops: There was an error trying to create a card')
            return None
        print('[from_passcode] Oops: There was an error trying to get card data')
        return None

    def __init__(self,json_data:list[dict]):
        self.__list_load(json_data)
        #self.__card_list = json_data

        #_codes = {
        #    str(y.get('id')): [
        #        x.get('id') for x in y.get('card_images') if isinstance(x,dict) and 'id' in x
        #    ] for y in json_data if isinstance(y,dict) and 'id' in y and 'card_images' in y
        #}
        #self.__passcodemap = _codes

        #_codes = {
        #    str(y.get('id')): [
        #        x.get('set_code') for x in y.get('card_sets') if isinstance(x,dict) and 'set_code' in x
        #    ] for y in json_data if isinstance(y,dict) and 'id' in y and 'card_sets' in y
        #}
        #self.__setcodemap = _codes

    def search(self,**kwargs):
        var_names = kwargs.keys()
        #print(var_names)
        if 'passcode' in var_names:
            print('[search] passcode search detected')
            code = kwargs.get('passcode')
            if isinstance(code,int):
                return self.__search_passcodes(code)
        elif 'set_code' in var_names:
            print('[search] set code search detected')
            code = kwargs.get('set_code')
            if isinstance(code,str):
                return self.__search_set_codes(code)

        print(f'[search] Oops: Invalid method arguments')
        return None


    def from_passcode(self,code:str|int):
        primary_code = self.__search_passcodes(code)
        if primary_code:
            return self.__get_card(primary_code,passcode=code)
            #_code2 = code if primary_code!=str(code) else None
            #card_stuff = self.__get_card_data(primary_code)
            #if card_stuff:
            #    card_type = card_stuff.get('type')
            #    card =  YGOExtraDeck(card_stuff,_code2) if any((x in card_type for x in ('Fusion','Synchro','Link','XYZ'))) \
            #                else YGOSpell(card_stuff,_code2) if 'Spell' in card_type \
            #                else YGOTrap(card_stuff,_code2) if 'Trap' in card_type \
            #                else YGOToken(card_stuff,_code2) if 'Token' in card_type \
            #                else YGOMonster(card_stuff,_code2) if 'Monster' in card_type \
            #                else None
            #    if card:
            #        return card
            #    print('[from_passcode] Oops: There was an error trying to create a card')
            #    return None
            #print('[from_passcode] Oops: There was an error trying to get card data')
            #return None
        print('[from_passcode] Oops: There is an error trying to find the primary passcode')
        return None
    
    def from_set_code(self,code:str):
        __passcode = self.__search_set_codes(code)
        if __passcode:
            return self.__get_card(__passcode,set_code = code)
        print('[from_set_codepasscode] Oops: There is an error trying to find the primary passcode')
        return None
    
    def num_cards(self):
        return len(self.__card_list)

if __name__=="__main__":
    fp = open('/home/bisneksual/Documents/pyugioh/db/sample/all.json','r')
    result = json.load(fp)
    card_data = result['data']

    cl =__YGOCardList(card_data)

    print(cl.search(passcode=90669991))
    card = cl.from_passcode(90669991)
    print(repr(card))

    print(cl.search(set_code="RATE-EN031"))
    card = cl.from_set_code("RATE-EN031")
    print(repr(card))