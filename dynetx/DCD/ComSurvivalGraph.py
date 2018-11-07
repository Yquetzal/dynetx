import networkx as nx

from dynetx.DCD.louvain import *
from dynetx.utils import dynamicCommunitiesSN
from dynetx.DCD.computingComsBySN import *

__author__ = "Giulio Rossetti"
__contact__ = "giulio.rossetti@gmail.com"
__website__ = "about.giuliorossetti.net"
__license__ = "BSD"

#coming from falkowsky : Mining and Visualizing the Evolution of Subgroups in Social Networks


def matchCommunitiesAccordingToCom(dynComSN,matchesGraph,*args):
    #find communities in the graph of matching
    node2comID = best_partition(matchesGraph,*args)
    #for each "node" (of this network of communities)
    for (t,c),cID in node2comID.items():
        #create an ID
        newComID = "DC_"+str(cID)
        #if this Id is already present, means that 2 communities of the SAME timestep are merged, modified the communities accordingly
        if newComID in dynComSN._communities[t].inv:
            dynComSN._communities[t].inv[newComID]=dynComSN._communities[t].inv[newComID].union(c)
            del dynComSN._communities[t][c]
        else: #remplace the ID of the (local) community by the ID of the (global) community
            dynComSN._communities[t][c]=newComID #add DC_ to avoid confusion with already assigned com ID




def jaccard(com1,com2):
    return float(len(com1 & com2)) / float(len(com1 | com2))

def build_matches_graph(partitions,mt):
    graph = nx.Graph()
    coms = partitions.communities()

    allComs = set()
    for t in coms:  # for each date taken in chronological order
       for c in coms[t]:
           allComs.add((t,c))


    for com1 in allComs:
        for com2 in allComs:
            if com1!=com2: #if not same community
                jac = jaccard(com1[1],com2[1])
                if jac>=mt:
                    commonNodes = len(com1[1] & com2[1])
                    identityPreservation = commonNodes / len(com1[1]) * commonNodes / len(com2[1])

                    graph.add_edge(com1,com2,weight=jac)#the weight is used such as the louvain algorihtm applied afterwards uses it (not sure it does)

    return graph


# def computePartitions(dynNetSN,CDalgo,*args):
#     coms = dynamicCommunitiesSN()
#     for SNt in dynNetSN.snapshots():
#         #partition = CDalgo(dynNetSN.snapshots(SNt), *args)
#
#         asNodeSets = {}
#         for n,c in partition.items():
#             asNodeSets.setdefault(c,set()).add(n)
#         #partition = {k: [v] for k, v in partition.items()}
#         for c in asNodeSets:
#             coms.addCommunity(SNt,asNodeSets[c])
#     return coms

def comSurvivalGraph(dynNetSN,mt=0.3,CDalgo="louvain",*args): #mt is the merge threashold. Algo can be either a networkx function returning communities of the string "louvain" to use louvain algorithm


    #print("computing survivalGraph with mt:",mt)

    #computing communities at each step using louvain
    #if isinstance(CDalgo,str):
    #    CDalgo=best_partition

    #print("survivalGraph: computing partitions")
    #dynComSN = computePartitions(dynNetSN,CDalgo,*args)
    dynComSN = normalLouvain(dynNetSN)

    matchesGraph = build_matches_graph(dynComSN,mt)

    matchCommunitiesAccordingToCom(dynComSN,matchesGraph,CDalgo,*args)

    dynComSN.createCustomEventGraph()

    return dynComSN

