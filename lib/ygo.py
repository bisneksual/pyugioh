import json
from constants import BANLIST_MAP,LINKMARKER_MAP
import re
from class_pyugioh import Card, Deck, Collection
import yaml
from configparser import ConfigParser
import os
from pathlib import Path
import requests
import itertools as it

class YGOCard(Card):
    #General Yu-Gi-Oh card class used to declare and manipulate all Yu-Gi-Oh cards
    #Data will be filled in using information from the YGOPRODECK API 
    #   (https://ygoprodeck.com/api-guide/)
    #Cards will have a primary passcode used for data lookup as well as a secondary 
    #   passcode or set code for deck reference purposes
    #Cards will have links to images but there is no system put in place for handling 
    #   API calls for images as laid out in the YGOPRODECK API guide
    
    #Constructor for YGOCard class where information is parsed at a foundational level
    #Information assigned here is generalized across almost all cards
    def __init__(self, data_card: dict,**kwargs):

        #Call superclass construtor to store raw data structure
        super().__init__(data_card)

        #Denotes that the card belongs to the Yu-Gi-Oh trading card game
        self.game = 'ygo'

        #Saves the dict of image URLs as a private property
        self.__images = self.get_data().get('card_images')

        #Access the data stored in the superclass for property initialization
        #It is important that this data is filled from the superclass property 
        #   instead of the argument passed into the constructor for data integrity 
        #   purposes.

        _data = self.get_data()

        #Clean the description text by getting rid  of single quotes and making the 
        #   bullet symbols ASCII friendly
        self.desc = _data.get('desc').replace("''","").replace('\u25cf','>')
        self.race = _data.get('race')

        self.hasArchetype = ('archetype' in _data)
        if self.hasArchetype:
            self.archetype = _data.get('archetype')

        _prices = _data.get('card_prices')[0]

        #Cast each value in the dict of card prices as a float before storing as a property
        if _prices:
            for shop in _prices:
                _prices[shop] = float(_prices[shop])
        self.prices = _prices

        #Build a list of possible passcodes based on the values of elements passed into 
        #   the images property
        #This is used to user inputted passcodes to the primary key used in database entries
        _codes = _data.get('card_images')
        _code_list = [x.get('id') for x in _codes if isinstance(x,dict) and 'id' in x]
        self.passcode_list = _code_list

        self.passcode = _data.get('id')

        #Create a list of information related to the sets that the card belongs to
        #This is used as an easier way to lookup and add cards as well as connect 
        #   cards that come from the same sets
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

        #Convert banlist data to an integer that represents the number of cards 
        #   allowed in a deck based on a certain ruleset
        _ban = _data.get('banlist_info')
        if _ban:
            _ban_map = {key.split('_')[-1]: BANLIST_MAP.index(_ban[key]) for key in _ban}
            self.banlist = _ban_map

        if 'passcode' in kwargs:
            self.secondaryPasscode = kwargs.get('passcode')
        
        if 'set_code' in kwargs:
            self.secondarySetCode = kwargs.get('set_code')

        #Delete the card json data just in case the garbage collector misses it
        del _data
    
    #Overriden method that returns a printout of important card information
    #Specifically, this will remove the inherited card data dict as well as the urls 
    #   for card images, the list of possible sets and price data
    def __repr__(self):
        vars = self.__dict__
        for key in ('_Card__data','_YGOCard__images','sets','prices'):
            if key in vars:
                del vars[key]

        return repr(vars)
    
    #Pretty prints the card data using the repr method
    #def pp(self):
    #    info = repr(self)
    #    return 

class YGOMonster(YGOCard):
    #Class meant specifically for Yu-Gi-Oh monster cards. This class is 
    #   specifically for monsters that belong to the Main Deck

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        #Assign the card type to a property
        self.cardType = 'monster'

        self.name = _data.get('name')
        self.frame = _data.get('frameType')
        self.types = _data.get('typeline')
        self.level = _data.get('level')
        self.attack = _data.get('atk')
        
        #Handle cases where a monster may not have an defense stat
        _def = _data.get('def')
        self.defense = _def if _def else 0
        self.attribute = _data.get('attribute')
        self.isPendulum = ('Pendulum' in _data.get('type'))

        #Add extra properties that exist solely for Pendulum monsters
        #These properties will have the prefix 'p'
        if self.isPendulum:

            self.pScale = _data.get('scale')

            #Save the pendulum description and the monster description separately, 
            #   making sure to overwrite the default description for the monster 
            #   description
            self.pDesc = _data.get('pend_desc')
            self.desc = _data.get('monster_desc').replace("''","")

        self.isTuner = ('Tuner' in _data.get('type'))
        
        #Add extra properties that exist solely for Ritual monsters
        #These properties will have the prefix 'r'
        self.isRitual = ("Ritual" in _data.get('type'))
        if self.isRitual:

            #Use regex to extract the Ritual card or archetype needed to summon the Ritual monster
            #TODO test capabilities of regex expression on existing Ritual monster descriptions
            _desc = self.desc
            _findritual = re.findall(r'Ritual Summon(?:ed)? (?:this card )?with .*"(.*?)"(?: Ritual Spell Card)?\.',_desc)
            self.rSummon = _findritual[0] if len(_findritual)>0 else ""

        self.isGemini = ('Gemini' in _data.get('type'))
        self.isUnion = ('Union' in _data.get('type'))
        self.isToon = ('Toon' in _data.get('type'))

        #Delete the card data placeholder in case the garbage collector misses it
        del _data

class YGOSpell(YGOCard):
    #Card class used specifically for Spell cards
    #The race property is renamed to mType to reduce confusion

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = 'spell'
        self.mType= _data.get('race')

        del _data

class YGOTrap(YGOCard):
    #Card class used specifically for Trap cards
    #The race property is renamed to tType to reduce confusion

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = 'trap'
        self.tType= _data.get('race')

        del _data

class YGOToken(YGOCard):
    #Card class used specifically for Token cards

    def __init__(self, data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        self.cardType = "token"

class YGOSkill(YGOCard):
    #Card class used specifically for Skill cards

    def __init__(self, data_card, **kwargs):
        super().__init__(data_card, **kwargs)

        self.cardType = 'skill'

class YGOExtraMonster(YGOMonster):
    #Card class used specifically for monsters that belong in the Extra Deck (i.e. Fusion, Synchro, Xyz, and Link)
    #A separate property for storing the type of Extra Deck monster will be created with the prefix 'x'

    def __init__(self,data_card,**kwargs):
        super().__init__(data_card,**kwargs)

        _data = self.get_data()

        self.cardType = "x_monster"

        #Add properties that exist only for Fusion monsters
        #These properties will have the prefix 'f'
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

class YGOCardList:

    def __list_load(self,data:list[dict]):
        self.__card_list = data
        #print('[__list_load] List loaded!')

        _codes = {
            str(y.get('id')): [
                x.get('id') for x in y.get('card_images') if isinstance(x,dict) and 'id' in x
            ] for y in data if isinstance(y,dict) and 'id' in y and 'card_images' in y
        }
        self.__passcodemap = _codes
        #print('[__list_load] passcode lookup map updated!')

        _codes = {
            str(y.get('id')): [
                x.get('set_code') for x in y.get('card_sets') if isinstance(x,dict) and 'set_code' in x
            ] for y in data if isinstance(y,dict) and 'id' in y and 'card_sets' in y
        }
        self.__setcodemap = _codes
        #print('[__list_load] set code lookup map updated!')

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
            card =  YGOExtraMonster(card_stuff,**kwargs) if any((x in card_type for x in ('Fusion','Synchro','Link','XYZ'))) \
                        else YGOSpell(card_stuff,**kwargs) if 'Spell' in card_type \
                        else YGOTrap(card_stuff,**kwargs) if 'Trap' in card_type \
                        else YGOToken(card_stuff,**kwargs) if 'Token' in card_type \
                        else YGOSkill(card_stuff,**kwargs) if 'Skill' in card_type \
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

    #TODO add fuzzy search capability for finding cards in cardlist

    def from_passcode(self,code:str|int):
        primary_code = self.__search_passcodes(code)
        if primary_code:
            return self.__get_card(primary_code,passcode=code)
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

class YGODeck(Deck):

    def __update_map(self):
        self.__deckmap = {key:self.__decklist.get(key) for key in ('main','extra','side','skill')}
        pass

    def __init__(self, deck_data, **kwargs):
        super().__init__(deck_data, **kwargs)
        _decklist = self._data.get('cards')
        #self.__main = _decklist.get('main')
        #self.__xtra = _decklist.get('extra')
        #self.__side = _decklist.get('side')
        #self.__skill = _decklist.get('skill')
        #self.__deckmap = (self.__main,self.__xtra,self.__side,self.__skill)
        self.__deckmap = {key:_decklist.get(key) for key in ('main','extra','side','skill')}
        #print(self.__deckmap)

    def get_cards(self):
        cards = {
            key: list(it.chain.from_iterable([
                [next(iter(card.keys()))] * int(next(iter(card.values()))) \
                if isinstance(card,dict) else [card]
                for card in _list
            ])) if _list else []
             for key, _list in self.__deckmap.items()
        }
        return cards
    
    def num_cards(self):
        card_counts = {
            key: sum(
                next(iter(card.values())) \
                    if isinstance(card,dict) and len(card.keys())==1 \
                    else 1
                for card in list
            ) if list else 0 \
            for key, list in self.__deckmap.items() \
        }
        return card_counts

    #def get_card()

    #TODO remove cards from deck
    #TODO find a way to retrieve cards from deck using passcode or set code, regardless of which version is stored in the deck

class YGOCollection(Collection):

    def __init__(self, coll_data):
        super().__init__(coll_data)
        

class YGODeckValidator:

    def __init__(self):
        pass

class PyugiohConfig:

    def __init__(self):
        self.__home_path = Path(__file__).parent.parent

        #print(self.__home_path)
        self.__config_path = os.path.join(self.__home_path,'config/pyugioh.ini')

        if os.path.isfile(self.__config_path):
            cparse = ConfigParser()
            cparse.read(self.__config_path)
            #print(cparse.sections())
            
            self.api_path = os.path.join(self.__home_path,cparse.get('ygo','api_path'))
            self.deck_path = os.path.join(self.__home_path,cparse.get('ygo','deck_path'))
        else:
            print('Oops. Config file not found.')

class YGODeckManager:

    def __deck_name_strip(self,deck_name:str):
        new_name = ''.join(char for char in deck_name.lower() if char.isalnum())
        return new_name

    def __update_decks(self):
        self.__decks = [p.name for p in Path(self.__deckpath).rglob("*") if p.is_file()]

    def __init__(self,path_to_decks:str):
        if not os.path.isdir(path_to_decks):
            os.mkdir(path_to_decks)
        self.__deckpath = path_to_decks
        self.__update_decks()
        pass

    def get_decks(self):
        return self.__decks
    
    def get_deck(self,deck_name:str):
        if self.deck_exists(deck_name):
            strip_name = self.__deck_name_strip(deck_name)
            with open(os.path.join(self.__deckpath,strip_name + ".deck"),'r') as fp:
                _deck_data = yaml.safe_load(fp)
            _deck = YGODeck(_deck_data)
            return _deck
        else:
            print(f"Deck '{strip_name}' does not exist.")
    
    def deck_exists(self,deck_name:str):
        strip_name = self.__deck_name_strip(deck_name)
        return f'{strip_name}.deck' in self.__decks

    def new_deck(self,deck_name:str,is_fantasy:bool = True, comment: str = ''):
        strip_name = self.__deck_name_strip(deck_name)
        path = os.path.join(self.__deckpath,strip_name + '.deck')
        if os.path.isfile(path):
            print(f"Deck '{strip_name}' already exists. Deck not created.")
        else:
            base_deck = {}
            base_deck['name'] = deck_name
            base_deck['fantasy'] = is_fantasy
            base_deck['comments'] = comment
            base_deck['cards']  =  []

            with open(path,'w') as fp:
                yaml.safe_dump(dict(deck=base_deck),fp)
            print(f"Deck '{strip_name}' created!")
        
        self.__update_decks()
        
    #TODO develop a way to add cards to a deck, validating against a collection

class APIManager:

    def __init__(self):
        pass

class Pyugioh:

    def __cardlist_load(self,path:str):
        path = self.config.api_path
        try:
            with open(path,'r') as fp:
                result = json.load(fp)
                card_data = result.get('data')

                self.cardlist = YGOCardList(card_data) if card_data else None
        except Exception as e:
            print(e)
            self.cardlist = None
    
    def __init_deckman(self):
        path = self.config.deck_path
        self.deckman = YGODeckManager(path)
        pass

    def __init_dataman(self):
        path = self.config.api_path
        self.dataman = APIManager()
        pass

    def __init__(self):
        self.config = PyugiohConfig()
        self.__cardlist_load(self.config.api_path)
        self.__init_deckman()
        self.__init_dataman()


if __name__=="__main__":

    pygo = Pyugioh()
    deck = pygo.deckman.get_deck('kaiba')
    print(deck.get_cards())
    print(deck.num_cards())

    #print(card.pp())

    #print(cl.search(set_code="SDK-001"))
    #card = cl.from_set_code("SDK-001")
    #print(card.pp())

    #with open('/home/bisneksual/Documents/pyugioh/example/kaiba_decklist.yaml','r') as deck:
    #    deck_info = yaml.safe_load(deck)
    
    #print(deck_info)