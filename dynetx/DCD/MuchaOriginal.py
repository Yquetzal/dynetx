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
    nodeOrder = list(Gs[0].nodes())
    N = len(nodeOrder)
    T = len(Gs)

    print("N", N)
    print("T", T)
    twomu = 0
    B = numpy.zeros(shape=(N * T, N * T))
    i = 1

    for g in Gs:
        gmat = nx.to_numpy_matrix(g, nodelist=nodeOrder)
        k = gmat.sum(axis=0)
        twom = k.sum(axis=1)
        twomu = twomu + twom
        indx = numpy.arange(start=0, stop=N) + numpy.array([(i - 1) * N] * N)

        nullModel = k.transpose() * k / twom
        B[numpy.ix_(indx, indx)] = gmat - nullModel  # for each slice, put the modularity matrix

        i += 1

    twomu = twomu + 2 * om * N * (T - 1)
    ones = numpy.ones((2, N * T))
    print(ones)
    diags = [-N, N]
    print(diags)
    omegaMat = scipy.sparse.spdiags(ones, diags, N * T, N * T)
    print(omegaMat.A)
    numpy.savetxt("test", omegaMat.A, fmt="%.2f")

    omegaMat = omegaMat * om
    print(omegaMat)
    B = B + omegaMat
    print(B)

    # matlab code
    S = runMatlabCode(B)
    print(S)


def runMatlabCode(matrix):
    dir = os.path.dirname(__file__)
    visuAddress = os.path.join(dir, "GenLouvain-master")


    matFormat = matlab.double(matrix.tolist())

    print("starting matlab engine")
    eng = engine.start_matlab()
    eng.addpath(visuAddress, nargout=0)
    print("matlab engine started successfully")

    print(matFormat)
    (S, Q) = eng.genlouvain(matFormat, nargout=2)
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



#preprocessMatrixForm(0.5)
#muchaOriginal("bla")