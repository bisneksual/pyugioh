import json
import ast

class Card:
    #Generic card class meant to represent all cards in library from all games

    __data = None
    game = None

    #Constructor class that ingests card data in dictionary form
    def __init__(self,data_card:dict):
        self.__data = data_card
    
    #returns card data dictionary cast as a dict
    def get_data(self):
        return dict(self.__data)

    def __str__(self):
        return str(self.__data)
    

    #Overriden method that returns a printout of important card information
    def __repr__(self):
        vars = self.__dict__
        return repr(vars)
    
    #Pretty prints the card data using the repr method
    def pp(self):
        return json.dumps(ast.literal_eval(repr(self)),indent=2)

class Deck:
    _data = None

    def __init__(self,deck_data:dict,**kwargs):
        self._data = deck_data.get('deck')
        self.name = self._data.get('name')
        self.comment = self._data.get('comments')
        #if "path_to_deck" in kwargs.keys:
        #    self.__path = 