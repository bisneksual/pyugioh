import yaml

class PyugiohConfig:

    def __init__(self) -> None:
        self.config = self.__init_config()

    def __init_config(self,path:str = "values.yaml") -> dict:
        with open(path,'w') as fp:
            return dict(yaml.safe_load(fp))
    