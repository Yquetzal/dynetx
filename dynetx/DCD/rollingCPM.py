import networkx as nx
from timeit import default_timer as timer
import dynetx as dn
from operator import itemgetter
from collections import defaultdict
from dynetx.utils import dynamicCommunitiesSN


__author__ = "Giulio Rossetti"
__contact__ = "giulio.rossetti@gmail.com"
__website__ = "about.giuliorossetti.net"
__license__ = "BSD"








def rollingCPM(dynNetSN,k=3):

    #print("computing PALLA with k: "+str(k))
    DynCom = dynamicCommunitiesSN()
    old_communities = None
    old_graph = nx.Graph()
    lastcid = 0
    tabDurations =[]
    graphs=dynNetSN.snapshots()
    for (date, graph) in graphs.items():
        #print("--- t:"+str(date))
        start = timer()
        communitiesAtT = list(_get_percolated_cliques(graph, k)) #get the percolated cliques (communities) as a list of set of nodes
        for c in communitiesAtT:
            DynCom.addCommunity(date, c)

        if old_communities == None: #if first snapshot
            old_graph = graph
            dateOld=date
            old_communities = communitiesAtT

        else:
            #communities = {res[idc-lastcid]: idc for idc in range(lastcid, lastcid+len(res))} #associate new IDs to com
            if len(communitiesAtT)>0: #if there is at least one community
                union_graph = nx.compose(old_graph, graph) #create the union graph of the current and the previous
                communities_union = list(_get_percolated_cliques(union_graph, k)) #get the communities of the union graph
                #communities_union = {res2[idc-lastcid]: idc for idc in range(lastcid, lastcid+len(res2))} #assign new IDs to coms of union graph

                #jaccardBeforeAndUnion = _jaccard_similarity(old_communities, communities_union,threashold=0.1) #we only care if the value is above 0
                #jaccardUnionAndAfter = _jaccard_similarity(communitiesAtT,communities_union,threashold=0.1) #we only care if the value is above 0
                jaccardBeforeAndUnion = _included(old_communities, communities_union) #we only care if the value is above 0
                jaccardUnionAndAfter = _included(communitiesAtT,communities_union) #we only care if the value is above 0


                for c in jaccardBeforeAndUnion: #for each community in the union graph
                    matched = []
                    born = []
                    killed = []

                    allJaccards = set()
                    for oldC in jaccardBeforeAndUnion[c]:
                        for newC in jaccardUnionAndAfter[c]:
                            allJaccards.add(((oldC,newC),_singleJaccard(oldC,newC))) #compute jaccard between candidates before and after
                    allJaccards = sorted(allJaccards, key=itemgetter(1), reverse=True)
                    sortedMatches = [k[0] for k in allJaccards]

                    oldCToMatch = dict(jaccardBeforeAndUnion[c]) #get all coms before
                    newCToMatch = dict(jaccardUnionAndAfter[c]) #get all new coms
                    while len(sortedMatches)>0: #as long as there are couples of unmatched communities
                        matchedKeys = sortedMatches[0] #pair of communities of highest jaccard
                        matched.append(matchedKeys) #this pair will be matched

                        del oldCToMatch[matchedKeys[0]] #delete chosen com from possible to match
                        del newCToMatch[matchedKeys[1]]
                        sortedMatches = [k for k in sortedMatches if len(set(matchedKeys) & set(k))==0] #keep only pairs of unmatched communities

                    if len(oldCToMatch)>0:
                        killed.append(list(oldCToMatch.keys())[0])
                    if len(newCToMatch)>0:
                        born.append(list(newCToMatch.keys())[0])

                    #print("checking",matched,killed,born,jaccardUnionAndAfter[c])
                    for aMatch in matched:
                        #print("check continue ",DynCom.getID(dateOld,aMatch[0]),DynCom.getID(date,aMatch[1]))
                        DynCom.addEvent((dateOld,DynCom.getID(dateOld,aMatch[0])),(date,DynCom.getID(date,aMatch[1])),dateOld,date,"continue")

                    for kil in killed:#these are actual merge (unmatched communities are "merged" to new ones)
                        for com in jaccardUnionAndAfter[c]:
                            #print("merge",kil,DynCom.getID(dateOld,kil),"=>",com,DynCom.getID(date,com))
                            #print("because",c)
                            #print("oups",jaccardBeforeAndUnion)
                            DynCom.addEvent((dateOld,DynCom.getID(dateOld,kil)),(date,DynCom.getID(date,com)),dateOld,date,"merged")

                    for b in born:#these are actual merge (unmatched communities are "merged" to new ones)
                        for com in jaccardBeforeAndUnion[c]:
                            DynCom.addEvent((dateOld,DynCom.getID(dateOld,com)),(date,DynCom.getID(date,b)),dateOld,date,"split")

            old_graph = graph
            dateOld=date
            old_communities = communitiesAtT

        end = timer()
        DynCom.relabelComsFromContinuousEvents()
    return(DynCom)

def _get_percolated_cliques(g, k):
    perc_graph = nx.Graph()
    cliques = [frozenset(c) for c in nx.find_cliques(g) if len(c) >= k]
    perc_graph.add_nodes_from(cliques)

    # First index which nodes are in which cliques
    membership_dict = defaultdict(list)
    for clique in cliques:
        for node in clique:
            membership_dict[node].append(clique)

    # For each clique, see which adjacent cliques percolate
    for clique in cliques:
        for adj_clique in _get_adjacent_cliques(clique, membership_dict):
            if len(clique.intersection(adj_clique)) >= (k - 1):
                perc_graph.add_edge(clique, adj_clique)

    # Connected components of clique graph with perc edges
    # are the percolated cliques
    for component in nx.connected_components(perc_graph):
        yield(frozenset.union(*component))

def _get_adjacent_cliques(clique, membership_dict):
    adjacent_cliques = set()
    for n in clique:
        for adj_clique in membership_dict[n]:
            if clique != adj_clique:
                adjacent_cliques.add(adj_clique)
    return adjacent_cliques

def _singleJaccard(set1,set2):
    return float(len(set1 & set2))/float(len(set1 | set2))
# @todo: check. Deve restituire il secondo dizionario in ingresso con le chiavi coerenti con il primo (intersezione massima)

def _jaccard_similarity( oldc, newc,threashold=0):
    newmapped = {}
    for c in newc:
        newmapped[c]={}
        for cd in oldc:
            jaccard = float(len(c & cd))/float(len(c | cd))
            if jaccard>=threashold:
                newmapped[c][cd]=jaccard
    return newmapped

def _included( smallers, largers):
    newmapped = {}
    for larger in largers:
        newmapped[larger]={}
        for smaller in smallers:
            if len(smaller & larger) == len(smaller):
                newmapped[larger][smaller]=len(smaller)
    return newmapped