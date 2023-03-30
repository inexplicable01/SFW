from .ModelObject import ModelObject, ModelType
from .Restrictor import Restrictor

class HT_Exchanger(ModelObject):

    def __init__(self, rname1, rname2, restrictors:list[Restrictor], name):
        ModelObject.__init__(self, name=name, mt = ModelType.HT_Exchanger)
        self.restrictor1 = None
        self.restrictor2 = None
        for r in restrictors:
            if r.name ==rname1:
                self.restrictor1 = r
            if r.name == rname2:
                self.restrictor2 = r
        if self.restrictor1 is None or self.restrictor2 is None:
            raise('Cannot find ' + rname1 + ' or '+ rname2 +' in restrictors.')

        ### Using NTU method for now.

    def NTU_HeatExchange(self):
        ## Assume both fluids are
        cpair = 1.006 # kJ/Kg/K
        Cp1 = self.restrictor1.mdot*cpair
        Cp2 = self.restrictor2.mdot*cpair
        MCP_Capacity = Cp1 if Cp1<Cp2 else Cp2
        U = 3433
        return U

