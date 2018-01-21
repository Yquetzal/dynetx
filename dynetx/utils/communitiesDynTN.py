from sortedcontainers import *
import networkx as nx
from .communitiesEventsHandler import *
from dynetx.utils.Intervals import *
from.fileReading import *


class dynamicCommunitiesTN:
    def __init__(self):
        self.nodes = {}
        self.communities = {}
        self.events=CommunitiesEvent()

    def addNodeComRelationship(self, n, com, t, e):
        n = str(n)
        self.nodes.setdefault(n,{}).setdefault(com,intervals()).addInterval((t,e))
        self.communities.setdefault(com, {}).setdefault(n,intervals()).addInterval((t,e))

    def addEvent(self,comsBefore, comsAfter,tBefore,tAfter,type):
        self.events.addEvent(comsBefore,comsAfter,tBefore,tAfter,type)

    def writeAsSGC(self, outputFile,renumber=False):  # SG => stream graph. format I use for my visualisation

        toWrite = []
        comFloatIDs = {}
        comIDs = 1
        for n in self.nodes:
            line = [str(n).replace(" ","_")]
            belongings = self.nodes[n]
            for com in belongings:
                if renumber:
                    if not com in comFloatIDs:
                        comFloatIDs[com] = comIDs
                        comIDs += 1
                else:
                    comFloatIDs[com]=com
                for boundaries in belongings[com].getIntervals():

                    # line.append(str(com.begin)+"_"+str(com.end-self.stepL)+":"+str(comFloatIDs[com.data]))
                    line.append(str(boundaries[0]) + "_" + str(boundaries[1]) + ":" + str(comFloatIDs[com]))
            toWrite.append(line)
        writeArrayOfArrays(toWrite, outputFile)

    def belongingsT(self,nBunch=None,cBunch=None): #return set of triplets (n,c,duration), or set of pairs of one of the parameters has a single value, or a single value if single node and single com
        toReturn={}
        if nBunch==None:
            nBunch=self.nodes.keys()
        if cBunch==None:
            cBunch=self.communities.keys()

        if isinstance(nBunch,str):
            nBunch=[nBunch]
        if isinstance(cBunch,str):
            cBunch=[cBunch]
        nBunch = set(nBunch)
        cBunch = set(cBunch)

        for n in nBunch:
            for c in cBunch & set(self.nodes[n]):
                toReturn[(n,c)]=self.nodes[n][c].duration()

        if len(nBunch)==1:
            toReturn = {c:t for (n,c),t in toReturn.items()}
        if len(cBunch)==1:
            toReturn = {n:t for (n,c),t in toReturn.items()}
        if len(nBunch)==1 and len(cBunch)==1:
            toReturn = list(toReturn.items)[0][1]
        return toReturn

    def writeEvents(self,outputFile):
        toWrite = []
        for (u,v,d) in self.events.edges(data=True):
            toWrite.append([d["time"][1],u,v,d["type"]])
        writeArrayOfArrays(toWrite, outputFile)
