import json
import ast

class Card:

    __data = None
    game = None

    def __init__(self,data_card:dict):
        self.__data = card_data
    
    def get_data(self):
        return dict(self.__data)

    def __str__(self):
        return str(self.__data)
    
    def __repr__(self):
        vars = self.__dict__
        del vars['_Card__data']
        del vars['_YGOCard__images']
        return repr(vars)
    
    def pp(self):
        return json.dumps(ast.literal_eval(repr(self)),indent=2)


class YGOCard(Card):
    
    def __init__(self, data_card: dict):
        super().__init__(data_card)
        self.game = 'ygo'
        self.__images = self.get_data().get('card_images')

        _data = self.get_data()
        self.desc = _data.get('desc').replace("''","")
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

        del _data

class YGOMonster(YGOCard):

    def __init__(self, data_card):
        super().__init__(data_card)

        _data = self.get_data()

        self.cardType = 'monster'
        self.name = _data.get('name')
        self.frame = _data.get('frameType')
        self.types = _data.get('typeline')
        self.level = _data.get('level')
        self.attack = _data.get('atk')
        self.defense = _data.get('def')
        self.attribute = _data.get('attribute')

        self.isPendulum = ('Pendulum' in _data.get('type'))

        if self.isPendulum:
            self.pScale = _data.get('scale')
            self.pDesc = _data.get('pend_desc')
            self.desc = _data.get('monster_desc').replace("''","")

        self.isTuner = ('Tuner' in _data.get('type'))

        del _data

if __name__=="__main__":
    fp = open('/home/bisneksual/Documents/pyugioh/db/sample/sample_card_pendulum.json','r')
    card = json.load(fp)
    card_data = card['data'][0]

    card = YGOMonster(card_data)
    print(card.pp())