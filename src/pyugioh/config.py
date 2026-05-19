import json

class Config(dict):
    
    #Config class, inherited from dictionary. Mainly used to read and
    # write config data into a dictionary structure to be passed into other
    # Pyugioh modules.

    def __init__(self,config_path:str='vol/config/config.json') -> None:
        #Overridden constructor. Reads config data from file and
        # initializes using the resulting dictionary.
        #config_path: the path to the config json file with the pyugioh
        # root folder as the working directory
        self.__path = config_path
        dict.__init__(self,self.read())

    def read(self) -> dict:
        #Reads the file in the path property and returns the contents,
        # usually to be initialized by the constructor
        #:returns: contents of the config folder in dictinoary format
        #:rtype: dict
        with open(self.__path,'r') as fp:
            config = json.load(fp)
        return dict(config)

    def write(self) -> None:
        #Writes the contents of the config object to the path property,
        # typically to overwrite config settings
        with open(self.__path,'w') as fp:
            json.dump(self,fp)