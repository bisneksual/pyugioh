

class ConnectorError(Exception):
    pass


class _Connector:
    def __init__(self):
        pass
    
    def connect(self):
        raise ConnectorError("connect() method of Connector class must be overridden.")
    
    def is_connected(self):
        raise ConnectorError("is_connected() method of Connector class must be overridden.")
    
    def query(self):
        raise ConnectorError("is_connected() method of Connector class must be overridden.")