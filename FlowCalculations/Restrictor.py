
from .ModelObject import ModelObject, ModelType
from .Chamber import Chamber

class Restrictor():
    def __init__(self, criticalarea, flowrate,name, flow_coefficent, upstreamchamber, downstreamchamber):
        ModelObject.__init__(self, name=name, mt = ModelType.Restrictor)
        self.criticalarea = criticalarea
        self.flowrate = flowrate
        self.flow_coefficent = flow_coefficent
        self.upstreamchamber:Chamber = upstreamchamber
        self.downstreamchamber:Chamber =downstreamchamber
        self.mdot = 0
        self.Ma =0