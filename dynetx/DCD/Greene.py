from dynetx.DCD.louvain import *
from dynetx.utils import dynamicCommunitiesSN

__author__ = "Giulio Rossetti"
__contact__ = "giulio.rossetti@gmail.com"
__website__ = "about.giuliorossetti.net"
__license__ = "BSD"


def matchAll(oldc, newc,mt):
    """
    oldc,newc : list of communities defined as dic {cID:set of nodesID}
    return dic {newC:oldC} communities not matched are missing
    """
    coms_matched = set()
    for c in oldc:  # for each of the new communities
        for cd in newc:  # for each of the old communities
            jaccard = float(len(oldc[c] & newc[cd])) / float(len(oldc[c] | newc[cd]))  # compute jaccard

            if jaccard >= mt:  # check if this jaccard is the best and above threashold k
                coms_matched.add((c,cd))
    return coms_matched  # return dic {newC:oldC} communities not matched are missing


def build_matches(partitions,mt):
    coms = partitions.communities()

    for i in range(len(coms) - 1):  # for each date taken in chronological order
        tOfSN = coms.iloc[i]
        nextTOfSN = coms.iloc[i + 1]

        oldc = partitions.communities(tOfSN)
        newc = partitions.communities(nextTOfSN)
        matched = matchAll(oldc.inv, newc.inv,mt)  # find the best match for each new commmunity

        for c in matched:  # c is the oldest community
            partitions.addEvent((tOfSN,c[0]),(nextTOfSN,c[1]),tOfSN,nextTOfSN,type="unknown")


def computePartitions(dynNetSN,CDalgo,*args):
    coms = dynamicCommunitiesSN()
    for SNt in dynNetSN.snapshots():
        partition = CDalgo(dynNetSN.snapshots(SNt), *args)
        asNodeSets = {}
        for n,c in partition.items():
            asNodeSets.setdefault(c,set()).add(n)
        #partition = {k: [v] for k, v in partition.items()}
        for c in asNodeSets:
            coms.addCommunity(SNt,asNodeSets[c])
    return coms

def greene(dynNetSN,mt=0.3,CDalgo="louvain",*args): #mt is the merge threashold. Algo can be either a networkx function returning communities of the string "louvain" to use louvain algorithm


    #print("computing Greene with mt:",mt)

    #computing communities at each step using louvain
    if isinstance(CDalgo,str):
        CDalgo=best_partition

    #print("Greene: computing partitions")
    dynPartitions = computePartitions(dynNetSN,CDalgo,*args)

    #print("Greene: matching communities")
    build_matches(dynPartitions,mt)
    #print("Greene: identify events")
    dynPartitions.relabelComsFromContinuousEvents(typedEvents=False)

    return dynPartitions
