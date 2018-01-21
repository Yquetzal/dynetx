import networkx as nx
import os
import sys
import dynetx as dn
import operator
import webbrowser


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

def write_SG(theDynGraph,fileOutput):
        toWrite = []
        toWrite.append(["LS", theDynGraph.start, theDynGraph.end])
        for (n, intervs) in theDynGraph.nodesD(t=None):
            toAdd = ["N", n.replace(" ","_")]
            #for interv in dataDic[n]:
            for interv in intervs.getIntervals():
                toAdd += [interv[0], interv[1]]
            toWrite.append(toAdd)


        for (n1,n2,intervs) in theDynGraph.edges():
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



    if sys.platform == "darwin":
        visuAddress = "file:///" + visuAddress
    webbrowser.get("firefox").open_new(visuAddress)