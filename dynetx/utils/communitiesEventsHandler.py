import networkx as nx
#from benchmarkGeneration.libs.Tools.usefulLinkStream import *
from pathlib import Path



class CommunitiesEvent(nx.DiGraph):
    def __init__(self):
        super(CommunitiesEvent, self).__init__()

    def addEvent(self,n1,n2,tBefore,tAfter,type,fraction=-1): #type can be merge, continue, split or unknown
        self.add_edge(n1,n2,time=(tBefore,tAfter),type=type,fraction=fraction)

    def addEvent_from(self, sources, dests, tBefore, tAfter,
                 type,fraction):  # type can be merge, continue, split or unknown
        for source in sources:
            if not source in dests:
                for dest in dests:
                    self.addEvent(source, dest, time=(tBefore, tAfter), type=type,fraction=fraction)

    def isNewBorn(self,c):
        return self.isNewbornFromVoid(c) or self.isNewbornFromMerge(c) or self.isNewbornFromSplit(c)

    def isNewbornFromVoid(self,c):
        return self.in_degree(c)==0

    def isNewbornFromMerge(self, c):
        if self.in_degree(c) <= 1:  # if no ancestor, not a split
            return False
        for pred in self.predecessors(c):  # for each ancestor
            if pred == c:  # if it is the same node (strange but who knows)
                return False

            #if isinstance(pred, tuple):  # if the community has an ID associated
             #   if pred[1] == c[1]:  # and the coms have the same IDs
              #      return False
        return True

    def mainSuccessor(self, ancestorCom,
                      allSuccessors):  # return the successor most probable of being the continutation of current com (in term of nm common nodes
        if len(allSuccessors) < 2:
            print("STRANGE: Ask for main ancestor while there is only one: %s" % allSuccessors)
            return -1
        similarity = {k: len(ancestorCom & allSuccessors[k]) for k in allSuccessors}
        maxVal = max(similarity.values())
        for k in similarity:
            if similarity[k] == maxVal:
                return k

    # def mainAncestor(self, allAncestors, successor):
    #     ###list
    #     ###{str:list)
    #     if len(allAncestors) < 2:
    #         raise Exception("Ask for main ancestor while there is only one")
    #     similarity = {k: len(successor & allAncestors[k]) for k in allAncestors}
    #     maxVal = max(similarity.values())
    #     for k in similarity:
    #         if similarity[k] == maxVal:
    #             return k

    def isNewbornFromSplit(self, c):
        if self.in_degree(c) == 0:  # if no ancestor, not a split
            return False

        for pred in self.predecessors(c):  # for each ancestor (case of strange com match)
            hasAValidPred = False
            if self.out_degree(pred) > 1:  # if it is a divide
                if pred == c:  # if it is the same node (strange but who knows)
                    return False

                #if isinstance(pred, tuple):  # if the community has an ID associated
                #    if pred[1] == c[1]:  # and the coms have the same IDs
                #        return False
                hasAValidPred = True
        if hasAValidPred:
            return True
        else:
            return False

    # def readAsEdgeGraph(self, file):
    #     my_file = Path(file)
    #     if my_file.is_file():
    #         self.events = DyNo.read_network_file(file, in_format="edges", directed=True)
    #     else:
    #         self.events = nx.Graph()
    #     print("read the event graph, edges : %s " % (self.events.number_of_edges()))
    #
    # def writeAsEdgeGraph(self, file):
    #     print("writing events as a network in :" + file)
    #     print(self.events.number_of_edges())
    #     print(len(self.events.nodes()))
    #
    #     DyNo.write_network_file(self.events, file, "edges", data=True)

    def writeAsTextual(
            self):  ##simple copy paste of the method that was implemented by Giulio in method Greene, need to be adapted
        print("TO DO")
        # for c in matches:
        # 	date = cid_to_date[c]
        # 	self.out.write("BIRTH\t%s\t%s\n" % (date, c))
        # 	for (t, m) in matches[c]:
        # 		self.out.write("MATCH\t%s\t%s\t%s" % (t, c, m))
        # 	self.out.flush()
        # self.out.close()