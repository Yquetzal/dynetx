from sortedcontainers import *
import networkx as nx
from .communitiesEventsHandler import *
from .communitiesDynTN import *
from .bidict import *
from operator import itemgetter
from collections import Iterable
class dynamicCommunitiesSN:
    def __init__(self):
        self._communities=SortedDict() #A sorted dict, key:time, value: bidict {frozenset of nodes}:id
        self.events=CommunitiesEvent()
        self.automaticID=1

    def addBelonging(self,n,t,cID): #be careful, if the n is a single node in the shape of a set, incorrect behavior
        if isinstance(t,str) or not isinstance(t,Iterable):
            t = set([t])
        if isinstance(cID,str) or not isinstance(cID,Iterable):
            cID = set([cID])
        if isinstance(n,str) or not isinstance(n,Iterable):
            n=frozenset([n])
        else:
            n = frozenset(n)



        for ts in t:
            if not ts in self._communities:
                self._communities[ts]=bidict()
            coms = self._communities[ts]
            for cs in cID:
                if not cs in coms.inv:
                    coms.inv[cs]=frozenset()
                coms.inv[cs]=coms.inv[cs].union(n)

    def addBelongins_from(self,clusters,t):
        """

        :param clusters: bidict{frozenset of nodes}:id
        :return:
        """
        self._communities[t]=clusters

    def addCommunity(self,t,com,id=None): #com is a community provided as a set/list of nodes
        com = frozenset(com)
        if id==None:
            id=str(self.automaticID)
            self.automaticID+=1
        self.addBelonging(com,t,id)
        #self._communities.setdefault(t, bidict())[com]=id

    def addEvent(self,comsBefore, comsAfter,tBefore,tAfter,type): #type can be merge, continue, split or unknown
        self.events.addEvent(comsBefore,comsAfter,tBefore,tAfter,type)

    def addEvent_from(self,comsBefore, comsAfter,tBefore,tAfter,type): #type can be merge, continue, split or unknown
        self.events.addEvent_from(comsBefore,comsAfter,tBefore,tAfter,type)

    def getID(self,t,com):
        return self._communities[t][com]

    def communities(self,t=None):
        if t==None:
            return self._communities
        return self._communities[t]

    def relabelComsFromContinuousEvents(self,typedEvents=True):
        if typedEvents:
            changedIDs = {} #
            for (u,v,d) in sorted(list(self.events.edges(data=True)),key=lambda x: x[2]["time"][0]):
                if d["type"]=="continue":

                    #update com ID in self
                    timeEnd = d["time"][1]
                    idComToChange = v[1]
                    idComToKeep = u[1]
                    if u in changedIDs:
                        idComToKeep = changedIDs[u]
                    changedIDs[v]=idComToKeep

                    nodesOfCom = self._communities[timeEnd].inv[idComToChange]
                    self._communities[timeEnd][nodesOfCom]=idComToKeep

                    #update com ID in event graph
                    nx.relabel_nodes(self.events, {(timeEnd,idComToChange): (timeEnd,idComToKeep)}, copy=False)

        if not typedEvents:
            #if events are not typed, we infer what we can, i.e one input and one input is a continue, otherwise we change label of edges accordingly
            for t in self._communities:
                for (c,cID) in self._communities[t].items():
                    nodeRef=(t,cID)
                    #print(self.events.out_degree([nodeRef]))
                    #print(self.events.nodes)
                    succ = self.events.out_degree([nodeRef])
                    if len(succ)>0 and succ[nodeRef]==1: #if only one successor

                        toMerge = next(self.events.successors(nodeRef))
                        if len(list(self.events.predecessors(toMerge)))==1: #if this successor has only one pred
                            #print("toMerge",toMerge)
                            #change label of event to continue:
                            self.events[nodeRef][toMerge]["type"]="continue"
                            nodesOfCom = self._communities[toMerge[0]].inv[toMerge[1]]
                            self._communities[toMerge[0]][nodesOfCom]=cID
                            nx.relabel_nodes(self.events,{toMerge:(toMerge[0],cID)},copy=False)
                    if len(succ)>0 and succ[nodeRef]>1:
                        for splitted in self.events.successors(nodeRef):
                            self.events[nodeRef][splitted]["type"] = "split"

                    pred = self.events.in_degree([nodeRef])
                    if len(pred)>0 and pred[nodeRef] > 1:
                        for merged in self.events.predecessors(nodeRef):
                            self.events[merged][nodeRef]["type"] = "merge"

    def convertToTNcommunities(self, convertTimeToInteger=False):
        dynComTN= dynamicCommunitiesTN()
        for i in range(len(self._communities)):
            if convertTimeToInteger:
                t=i
                tNext=i+1
            else:
                t = self._communities.peekitem(i)[0]
                if i<len(self._communities)-1:
                    tNext=self._communities.peekitem(i + 1)[0]
                else:
                    tNext = self._communities.peekitem("END")[1]

            for (c,cID) in self._communities.peekitem(i)[1].items(): #for each community for this timestep
                for n in c:#get the nodes, not the
                    dynComTN.addBelonging(n, cID, t, tNext)


        #convert also events
        for (u,v,d) in self.events.edges(data=True):
            if d["type"]!="continue": #if communities have different IDs
                dynComTN.addEvent(u[1],v[1],d["time"][0],d["time"][1],d["type"])
        return dynComTN
