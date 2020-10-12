
class UnicornException(Exception):
    def __init__(self, name: str,messages:str):
        self.name = name
        self.messages=messages
