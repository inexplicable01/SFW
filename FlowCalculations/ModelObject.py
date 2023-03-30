from enum import Enum

class ModelType(Enum):
    Chamber = 1
    Restrictor = 2
    HT_Exchanger = 3


class ModelObject():
    def __init__(self, name, mt):
        self.name = name
        self.modeltype: ModelType = mt