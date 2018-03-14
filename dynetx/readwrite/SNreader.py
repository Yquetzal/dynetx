import networkx as nx
import os
import sys
import dynetx as dn
import operator
import webbrowser
from sortedcontainers import *
from dynetx.utils.bidict import *
import numpy as np


def detectAutomaticallyFormat(networkFile):
    format = networkFile.split(".")[1]
    return format


def _write_network_file(graph, out_name, out_format="edges", data=False):
    """
    Write the graph representation on file using a user specified format

    :param graph: networkx graph
    :param out_name: pattern for the output filename
    :param out_format: output format. Accepted values: edgelist|ncol|gefx|gml|pajek
    """

    if out_format==None:
        out_format="edges"
    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    print("writing graph of format " + out_format + " at " + out_name)
    if out_format == 'edges':
        nx.write_edgelist(graph, "%s" % (out_name), data=data)
    elif out_format == 'gefx':
        nx.write_gexf(graph, "%s.gefx" % (out_name))
    elif out_format == 'gml':
        nx.write_gml(graph, "%s.gml" % (out_name))
    elif out_format == 'pajek':
        nx.write_pajek(graph, "%s.pajek" % (out_name))
    elif out_format == 'ncol':
        nx.write_edgelist(graph, "%s.ncol" % (out_name), delimiter='\t')
    elif out_format == 'GraphML':
        g = nx.write_graphml(out_name)
    else:
        raise Exception("UNKNOWN FORMAT " + out_format)


def _read_network_file(in_name, in_format="", directed=False):
    """
    Read the graph representation on file using a user specified format

    :param in_name: pattern for the output filename
    :param in_format: output format. Accepted values: edgelist|ncol|gefx|gml|pajek
    """

    if in_format == 'edges':
        if directed:
            g = nx.read_edgelist(in_name, create_using=nx.DiGraph())
        else:
            g = nx.read_edgelist(in_name, data=False)
    elif in_format == 'gefx':
        g = nx.read_gexf(in_name)
    elif in_format == 'gml':
        g = nx.read_gml(in_name)
    elif in_format == 'graphml':
        g = nx.read_graphml(in_name)
        nodesInfo = g.nodes(data=True)
        node2Label = {nodeid: data["label"].replace(" ","_") for (nodeid, data) in nodesInfo}
        g = nx.relabel_nodes(g, node2Label, copy=False)
    elif in_format == 'pajek':
        g = nx.read_pajek(in_name)
    elif in_format == 'ncol':
        g = nx.read_edgelist(in_name)
    else:
        raise Exception("UNKNOWN FORMAT " + in_format)
    return g


####################READ WRITE OPERATIONS##################
def readSnapshotsDir(inputDir, format=None):


    anSnGraph = dn.DynGraphSN()
    files = os.listdir(inputDir)
    visibleFiles = [f for f in files if f[0] != "."]

    if format==None:
        format=detectAutomaticallyFormat(visibleFiles[0])

    for f in visibleFiles:
        g = _read_network_file(inputDir + "/" + f, format)  # type:nx.Graph
        anSnGraph.addSnaphsot(os.path.splitext(f)[0],g)


    return anSnGraph


def writeSnapshotsDir(dynGraph,outputDir,format=None):
    if format==None:
        format="edges"
    allGraphs = dynGraph.snapshots()
    for g in allGraphs:
        _write_network_file(allGraphs[g],os.path.join(outputDir,str(g)+"."+format),out_format=format)

def write_SG(theDynGraph:dn.DynGraphTN,fileOutput):
        toWrite = []
        toWrite.append(["LS", theDynGraph.start, theDynGraph.end])
        for (n, intervs) in theDynGraph.nodesD().items():
            if type(n)is str:
                toAdd = ["N", n.replace(" ","_")]
            else:
                toAdd = [n]
            #for interv in dataDic[n]:
            for interv in intervs.getIntervals():
                toAdd += [interv[0], interv[1]]
            toWrite.append(toAdd)


        for ((n1,n2),intervs) in theDynGraph.edgesD().items():
            toAdd = ["E",n1,n2]
            if type(n1) is str:
                toAdd = ["E", n1.replace(" ","_"), n2.replace(" ","_")]
            for interv in intervs.getIntervals():
                toAdd += [interv[0], interv[1]]
            toWrite.append(toAdd)
        dn.writeArrayOfArrays(toWrite, fileOutput, separator="\t")

def writeGoodNodeOrder(theDynCom,fileOutput):
        node2Com = {}
        for n in theDynCom.nodes:
            belongings = theDynCom.belongingsT(n) #for each community, belonging duration
            ordered = sorted(belongings.items(), key=operator.itemgetter(1))
            ordered.reverse()
            node2Com[n.replace(" ","_")] = ordered[0][0] #assigne to each node its main com

        allMainComs = sorted(set(node2Com.values()))

        thefile = open(fileOutput, 'w')
        for c in allMainComs:
            for n in node2Com:
                if node2Com[n] == c:
                    thefile.write(n+"\n")
        thefile.close()

def show(dynCommunities,dynGraph):
    dir = os.path.dirname(__file__)

    if not isinstance(dynCommunities,dn.dynamicCommunitiesTN):
        dynCommunities = dynCommunities.convertToTNcommunities(convertTimeToInteger=True)
    if not isinstance(dynGraph,dn.DynGraphTN):
        dynGraph = dynGraph.toDynGraphTN()


    visuAddress = os.path.join(dir, "visu/LinkStream.html")

    dn.write_SG(dynGraph, os.path.join(dir,"visu/networks/netData/network.sg"))
    dynCommunities.writeAsSGC(os.path.join(dir,"visu/networks/netData/Communities/coms.sgc"))
    dynCommunities.writeEvents(os.path.join(dir,"visu/networks/netData/Communities/events.evts"))
    dn.writeGoodNodeOrder(dynCommunities, os.path.join(dir,"visu/networks/netData/nodeOrder"))

    visuAddress = "file:///" + visuAddress

    if sys.platform == "darwin":
        #visuAddress = "http://127.0.0.1:8000/" + visuAddress
        webbrowser.get("firefox").open_new(visuAddress)
    else:
        if sys.platform== "win32":
            if not "firefox" in webbrowser._tryorder:
                fpath = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(fpath))
        else:
            webbrowser.get("firefox").open_new(visuAddress)

def writeAsOrderedModifList(dynNet:dn.DynGraphTN, fileOutput,dateEveryLine=False,nodeModifications=False,separator="\t",edgeIdentifier="l"): #OML
        """
        OML :ordered modif list with dates as #DATE and no nodes (Online Modification List)
        OMLN : with nodes
        OMLR : with repeated dates
        OMLRN : nodes and repeated dates
        :param dateEveryLine: if true, date is repeated for each modification (each line). If false, date modification is on its own line (#DATE)
        before the modifications happening at this date
        """

        if type(dynNet) is dn.DynGraphSN:
            dynNet = dynNet.toDynGraphTN()

        timeOfActions = SortedDict()
        #NOTE : can be easily optimized ! one complete check to add and to remove nodes...
        dataDicNodes={}
        if nodeModifications: #note that we add nodes before edges, so that nodes are added before there edges...
            dataDicNodes = dynNet.nodesD()

            for (n,intervs) in dataDicNodes.items():
                #times = self.nodes[n]
                for interv in intervs.getIntervals():
                    addDate = interv[0]
                    #delDate = maxInterval(interv)
                    timeOfActions.setdefault(addDate,[]).append("+n" + separator + str(n))

        dataDicEdges = dynNet.edgesD()

        for (e,intervs) in dataDicEdges.items():
            #print("e",e,intervs)
            #times = self.edges[e]
            for interv in intervs.getIntervals():
                addDate = interv[0]
                delDate = interv[1]
                (node1, node2) = list(e)
                if not addDate in timeOfActions:
                    timeOfActions[addDate] = []
                if not delDate in timeOfActions:
                    timeOfActions[delDate] = []
                timeOfActions[addDate].append("+"+edgeIdentifier+separator + str(node1) + separator + str(node2))
                timeOfActions[delDate].append("-"+edgeIdentifier+separator + str(node1) + separator + str(node2))

        if nodeModifications:  # note that we remove nodes after edges,...
            for (n,intervs) in dataDicNodes.items():
                #times = self.nodes[n]
                for interv in intervs.getIntervals():
                    delDate = interv[1]

                    if not delDate in timeOfActions:
                        timeOfActions[delDate] = []
                    timeOfActions[delDate].append("-n" + separator + str(n))

        #(orderedKeys, orderedValues) = fromDictionaryOutputOrderedKeysAndValuesByKey(timeOfActions)
        toWrite = []
        for k in timeOfActions: #sorted because sorteddict
            if not dateEveryLine:
                toWrite.append(["#" + str(k)])
            for val in timeOfActions[k]:
                if dateEveryLine:
                    val+=separator+str(k)
                toWrite.append([val])

        dn.writeArrayOfArrays(toWrite, fileOutput, separator="\t")


def readListOfModifCOM(inputFile):
    dynCom = dn.dynamicCommunitiesTN()
    f = open(inputFile)
    endDate = -1
    date = -1
    setComsThisStep = set()
    for l in f:
        l = l.rstrip().split("\t")
        action = l[0]
        if "#" in action:
            setComsThisStep = set()
            date = float(action[1:])
            endDate = date

        if action == "+nc":
            node = l[1]
            com = l[2]
            #if not com in self.communities:
            #    setComsThisStep.add(com)
            dynCom.addBelonging(node,com,date)

        if action == "-nc":
            node = l[1]
            com = l[2]
            dynCom.removeBelonging(node, com,date)

        if action == "=":
            conserved = l[1]
            removed = l[2]
            dynCom.addEvent(conserved+removed,conserved,date,date,"merge")

    # endDate = endDate+infoSN.getStepL()
    #if infoSN != None:
    #    endDate += infoSN.getStepL()
    #self.endPeriod(endDate)

    return dynCom


def _readStaticSNByCom(inputFile, commentsChar="#", nodeSeparator=" ", nodeInBrackets=False,
                       mainSeparator="\t", comIDposition=0, nodeListPosition=1):
    """
    nodeSeparator: characters that separate the list of nodes
    nodeInBrackets : if true, list of nodes in the community is [x y z] instead of just x y z
    mainSeparator : character used to separate comID from nodesIDS
    """

    #read community file from a static network
    # if asSN:
    #     theDynCom = dn.dynamicCommunitiesSN()
    # if asTN:
    #     theDynCom = dn.dynamicCommunitiesTN()
    coms = bidict()
    f = open(inputFile)

    for l in f:  # for each line
        currentCom = set()
        if not l[0] == commentsChar:  # if it is not a comment line
            l = l.rstrip().split("\t")
            comID = l[comIDposition]
            nodesIDs = l[nodeListPosition]
            if len(nodesIDs)>=1:
                # if nodeInBrackets:
                if "[" in nodesIDs:
                    nodesIDs = nodesIDs[1:-1]
                if ", " in nodesIDs:
                    nodeSeparator = ", "
                for n in nodesIDs.split(nodeSeparator):
                    currentCom.add(n)
                    # if asSN:
                    #     theDynCom.addBelonging(n,startTime,comID)
                    # if asTN:
                    #     theDynCom.addBelonging(n,comID,startTime) #belongings without end
                coms[frozenset(currentCom)]=comID
    return coms


def readLinkStream(inputFile, toSN=True):  # SOCIOPATTERN format
    """
    this format is a variation of snapshots, in which all snapshots are in a single file, adapted for occasional observations
    at a high framerate (each SN is meaningless), Line Graph
    """
    theDynGraph = dn.DynGraphSN()
    f = open(inputFile)
    endDate = -1
    date = -1
    setComsThisStep = set()
    for l in f:
    # nodeList = []
    # start = inf
    # end=-inf
        date = float(l[0])
        n1 = l[1]
        n2 = l[2]
        #theDynGraph.add_interaction(n1,n2,date,date+intervalsToAdd)
        if toSN:
            theDynGraph.add_interaction(n1,n2,date)
    return theDynGraph


def readSNByCom(inputDir, nameFilter=None, **kwargs):
    """

    :param inputDir:
    :param nameFilter: a function that takes a file name and decript it into a
    :param kwargs:
    :return:
    """
    theDynCom = dn.dynamicCommunitiesSN()
    files = os.listdir(inputDir)
    visibleFiles = [f for f in files if f[0] != "."]
    timeIDs = SortedDict() #a dictionary associating timeIds to files
    if nameFilter!=None:
        for f in visibleFiles:
            timeID = nameFilter(f)
            if timeID!=None:
                timeIDs[timeID]=f

        #visibleFiles = timeIDs.keys()
    print("reading communities, ordered files:")
    print(timeIDs.keys())
    currentComIDs = 0

    for t in timeIDs:  # for each file in order of their name
        f = inputDir + "/" + str(timeIDs[t])
        coms = _readStaticSNByCom(f,**kwargs)
        #print(coms)
        theDynCom.addBelongins_from(coms,t)
    return theDynCom


def readStaticSNByNode(inputFile,separator="\t"):
    coms = dict()
    f = open(inputFile)
    for l in f:

        l = l.rstrip().split(separator)
        for com in l[1:]:
            comID = com
            coms.setdefault(comID,set()).add(l[0])
            #self.addNodeComRelationship(l[0], comID, startTime, stepL)
    toReturn = bidict()
    for com,nodes in coms.items():
        toReturn[frozenset(nodes)]=com

    return toReturn
