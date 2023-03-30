from .Chamber import Chamber
from .Restrictor import Restrictor
from .HT_Exchanger import HT_Exchanger

# import math
import time

# class FlowToResolve():
#     def __init__(self, name, restrictor:Restrictor):
#         self.name = name
#         self.restrictor = restrictor
#         self.upstreamchamber:Chamber = None
#         self.downstreamchamber:Chamber =None
#         self.mdot = 0
#         self.Ma =0




y = 1.4
R = 1716
g = 32.2

def isentropicMa(Pt,Ps):
    expoy = (y-1)/y
    Ma = (2/(y-1)* ( (Pt/Ps)**expoy- 1) )**0.5
    return abs(Ma)

class FlowModel():

    def __init__(self, chambers:list[Chamber], restrictors:list, ht_exchangers:list[HT_Exchanger]):
        self.chambers = chambers

        # self.flowsToResolve = {}
        self.ht_exchangers:list[HT_Exchanger] =ht_exchangers
        self.restrictors:list[Restrictor]=restrictors
        # self.chambernetwork = {}
        ## Restrictors can only have ONE in and ONE out  Chambers can have multple ins and mutiple out.
        # for r in self.restrictors:
        #     self.flowsToResolve[r.name] = FlowToResolve(r.name, r)
        #     for conn in connections:
        #         ##Look for relevant chambers   A restrictor can only have an upstream and downstream.  Checking for this should be added ****Important Improvement********
        #         if r == conn.second:
        #             self.flowsToResolve[r.name].upstreamchamber = conn.first
        #         if r == conn.first:
        #             self.flowsToResolve[r.name].downstreamchamber = conn.second
        for c in self.chambers:
            # self.chambernetwork[c.name] = ChambersLocalNetwork(c.name, c)
            for r in self.restrictors:
                if c == r.downstreamchamber:
                    c.upstreamflows.append(r)
                    c.upstreamchambers.append(r.upstreamchamber)
                elif c== r.upstreamchamber:
                    c.downstreamflows.append(r)
                    c.downstreamchambers.append(r.downstreamchamber)
        for c in self.chambers:
            if len(c.upstreamflows) ==0:
                c.issourcechamber =True
            elif len(c.downstreamflows) ==0:
                c.issinkchamber = True




    def InitialGuess(self):
        ##Build Chamber

        # for c in self.chambers:
        #     for name, ftr in self.flowsToResolve.items():
        #         if c ==ftr.upstreamchamber:
        #             c.downstreamchamber = ftr.downstreamchamber
        #         elif c == ftr.downstreamchamber:
        #             c.upstreamchamber = ftr.upstreamchamber


        for c in self.chambers:
            if c.pressure_needsguessing:
                ##Make a guess
                c.staticpressure = c.PressureGuess()
            if c.temp_needsguessing:
                ##Make a guess
                c.temperature = c.PressureGuess()


    def Solve(self):
        ### Solve for all mass flows

        ### Needs flow continuity
        for i_guess in range(1,20000):
            for r in self.restrictors:
                A_crit = r.criticalarea
                headPs = r.upstreamchamber.staticpressure
                downPs = r.downstreamchamber.staticpressure
                Tt = r.upstreamchamber.temperature

                cd = r.flow_coefficent

                ### Assume headstaticpressure = headtotalpressure if velocity is not given
                Ptup = headPs
                Ptdown = downPs
                # Ptdown = (Ptup-Ptdown)*Pt_Loss


                if downPs>Ptup:
                    Ma = isentropicMa(downPs, Ptup)
                    if Ma>1:
                        Ma =1
                    mideal = (-1)*A_crit * Ptup / (Tt ** 0.5) * (y / R) * Ma * (1 + (y - 1) / 2 * Ma ** 2) ** (
                                -(y + 1) / (2 * (y - 1))) * g
                else:
                    Ma = isentropicMa(Ptup, downPs)
                    if Ma>1:
                        Ma =1
                    mideal = A_crit * Ptup / (Tt ** 0.5) * (y / R) * Ma * (1 + (y - 1) / 2 * Ma ** 2) ** (
                                -(y + 1) / (2 * (y - 1))) * g
                # print(Ma)

                r.mdot = mideal*cd
                r.Ma = Ma
                heat = False
                for ht in self.ht_exchangers:
                    if ht.restrictor1 == r or ht.restrictor1 == r:
                        heat = True

                if heat:
                    r.downstreamchamber.temperature = r.upstreamchamber.temperature
                else:
                    r.downstreamchamber.temperature = r.upstreamchamber.temperature





            for c in self.chambers:
                if c.issinkchamber or c.issourcechamber:
                    continue
                incomingflow = 0
                outgoingflow = 0
                for r in c.upstreamflows:
                    flow = r.mdot
                    incomingflow = incomingflow + flow
                for r in c.downstreamflows:
                    flow = r.mdot
                    outgoingflow = outgoingflow + flow
                flowdiscontiunity = incomingflow-outgoingflow
                print("Iteration {:.0f}, Chamber {}, Incoming Flow {:.4f}, Outgoing Flow {:.4f}, Flow Discountiuous by {:.5f}, Static Pressure {:.2f} ".format(i_guess,c.name,incomingflow,outgoingflow,flowdiscontiunity,c.staticpressure))


                ### multi variable converger.?!
                if abs(flowdiscontiunity)>0.0001:
                    if incomingflow>outgoingflow: ##
                        ##Pressure needs to go up
                        c.staticpressure = c.staticpressure + 0.0005
                    else:
                        c.staticpressure = c.staticpressure - 0.0005
            print()

                    ##PRessure needs to go down.
                # raise('Mass not conversed at ' + cname)
            # time.sleep(0.01)


    def PrintResults(self):
        for r in self.restrictors:
            print("Restrictor {} has mass flow : {:.5f} and Ma of : {:.2f}".format(r.name,r.mdot,r.Ma))
        for c in self.chambers:
            print("Chamber {} has pressure : {:.2f} and Temperature of : {:.0f}".format(c.name,c.staticpressure,c.temperature))








