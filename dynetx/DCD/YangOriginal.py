import networkx as nx
import matlab
from matlab import engine
import numpy
import scipy
import matplotlib
from dynetx.DCD.louvainModified import best_partition
from dynetx.utils import dynamicCommunitiesSN
import os


###############################
######For this class, it is necessary to have Matlab installed
######And to set up the matlab for python engine, see how to there
###### https://fr.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
###### (you can find the value of matlabroot by tapping matlabroot in your matlab console)
################################

def preprocessMatrixForm(om):
    #initialisation inspired by http://netwiki.amath.unc.edu/GenLouvain/GenLouvain

    Gs = [nx.karate_club_graph(), nx.karate_club_graph()]
    GsMat = [nx.to_numpy_matrix(mat).tolist() for mat in Gs]
    nodeOrder = list(Gs[0].nodes())

    SocNet = dict()
    #SocNet["W"]=matlab.double(numpy.stack(GsMat).tolist())
    stacked = numpy.stack(GsMat)
    listed = stacked.tolist()
    SocNet["W"]=matlab.double(listed)

    SocNet["n"] = len(nodeOrder)
    SocNet["T"]=len(GsMat)
    SocNet["cellW"]=[]
    SocNet["Index"]=[]

    K=5

    net=dict()
    net["type"]="binary"
    net["wthrehold"]=-1 #ignored
    net["para"]=[]
    net["Temp"]=matlab.double(numpy.arange(1,-0.1,-0.1).tolist())#"1:-0.1:0"
    net["N"]=matlab.double([20]*2+[10]*5+[5]*4)#"[20*ones(1,2) 10*ones(1,5) 5*ones(1,4)]"
    net["Z"]=[]
    net["verbosity"]=1
    net["objfunc"]=[]




    # matlab code
    S = runMatlabCode(SocNet,K,net)
    print(S)


def runMatlabCode(SocNet,K,net):
    dir = os.path.dirname(__file__)
    visuAddress = os.path.join(dir, "YangOriginal")


    #matFormat = matlab.double(matrix.tolist())

    print("starting matlab engine")
    eng = engine.start_matlab()
    eng.addpath(visuAddress, nargout=0)
    print("matlab engine started successfully")

    #print(matFormat)
    (S, Q) = eng.SBMDynamicEvolutionOfflineDynamic2(SocNet,K,net)
    return(S)
    # S = numpy.asarray(S).reshape(2, 34)

def muchaOriginal(dynNetSN, om=0.5,form="local"):
    #print("INITIALISING MUCHA ")

    #dynNetSN.remove_nodes_from(dynNetSN.isolates())


    graphs = dynNetSN.snapshots()

    nodeOrderAllSN = []
    listModularityMatrices = []
    #graphs = {"A":nx.karate_club_graph(), "B":nx.karate_club_graph()}
    for i,gT in enumerate(graphs):
        g=graphs[gT]
        nodeOrder = list(g.nodes())
        nodeOrderAllSN.extend((i,n) for n in nodeOrder)

        gmat = nx.to_numpy_matrix(g, nodelist=nodeOrder)
        k = gmat.sum(axis=0)
        twom = k.sum(axis=1)
        nullModel = k.transpose() * k / twom
        listModularityMatrices.append(gmat - nullModel)

    #Concatenate all null modularity matrices
    B = scipy.linalg.block_diag(*listModularityMatrices)

    #add the link between same nodes in different timestamps
    multipleAppearances={} #for each node, list of indices where it appears
    for (i,(t,n)) in enumerate(nodeOrderAllSN):
        multipleAppearances.setdefault(n,[]).append(i)

    for (n,nAppearences) in multipleAppearances.items():
        for i in nAppearences:
            for j in nAppearences:
                if i!=j:
                    B[i,j]=om

    numpy.savetxt("test.csv", B, fmt="%.2f", delimiter=",")

    S = runMatlabCode(B)

    DCSN = dynamicCommunitiesSN()
    for i in range(len(S)):
        DCSN.addBelonging(nodeOrderAllSN[i][1],nodeOrderAllSN[i][0],S[i])
    return DCSN



preprocessMatrixForm(0.5)
#muchaOriginal("bla")