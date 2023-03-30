
from .ModelObject import ModelObject, ModelType

def Average(lst):
    return sum(lst) / len(lst)

class Chamber(ModelObject):

    def __init__(self, staticpressure, temperature, name):
        ModelObject.__init__(self, name=name, mt = ModelType.Chamber)
        self.staticpressure:float = staticpressure
        self.temperature:float = temperature
        self.staticpressureguess:bool = False
        self.issourcechamber = False
        self.issinkchamber = False
        self.upstreamflows = []
        self.downstreamflows = []
        self.upstreamchambers = []
        self.downstreamchambers = []

        if self.staticpressure==None:
            self.pressure_needsguessing = True
        else:
            self.pressure_needsguessing = False
        if self.temperature==None:
            self.temp_needsguessing = True
        else:
            self.temp_needsguessing = False

    def PressureGuess(self):
        pressval =[]
        for upc in self.upstreamchambers:
            if upc.staticpressure is not None:
                pressval.append(upc.staticpressure)
        for downc in self.downstreamchambers:
            if downc.staticpressure is not None:
                pressval.append(downc.staticpressure)
        if len(pressval)>0:
            return Average(pressval)
        else:
            return 15.0

    def TemperatureGuess(self):
        temperatureval =[]
        for upc in self.upstreamchambers:
            if upc.temperature is not None:
                temperatureval.append(upc.temperature)
        for downc in self.downstreamchambers:
            if downc.staticpressure is not None:
                temperatureval.append(downc.temperature)
        if len(temperatureval)>0:
            return Average(temperatureval)
        else:
            return 293

