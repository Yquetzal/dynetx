from dynetx.DCD.louvain import *
from dynetx.utils import dynamicCommunitiesSN


def normalLouvain(dynNetSN,):
    coms = dynamicCommunitiesSN()
    for SNt in dynNetSN.snapshots():
        partition = best_partition(dynNetSN.snapshots(SNt))
        asNodeSets = {}
        for n,c in partition.items():
            asNodeSets.setdefault(c,set()).add(n)
        for c in asNodeSets:
            coms.addCommunity(SNt,asNodeSets[c])
    return coms


def smoothedLouvain(dynNetSN):
    coms = dynamicCommunitiesSN()
    previousPartition = None
    for SNt in dynNetSN.snapshots():
        currentSN = dynNetSN.snapshots(SNt)

        if previousPartition!=None:
            #remove from the partition nodes that disappeared
            disappearedNodes = set(previousPartition.keys())-set(currentSN.nodes())
            for n in disappearedNodes:
                previousPartition.pop(n)

            #add to the partition nodes that appeared
            addedNodes = set(currentSN.nodes())-set(previousPartition.keys())
            maxCom = max(previousPartition.values())
            for n in addedNodes:
                maxCom+=1
                previousPartition[n]=maxCom



        partition = best_partition(currentSN,   partition=previousPartition)
        asNodeSets = {}

        for n,c in partition.items():
            asNodeSets.setdefault(c,set()).add(n)

        for c in asNodeSets:
            coms.addCommunity(SNt,asNodeSets[c])
        previousPartition=partition

    return coms