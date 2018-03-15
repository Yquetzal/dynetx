import unittest
import dynetx as dn
import os
import dynetx.DCD as DCD
from networkx.algorithms import community
import networkx as nx
from sortedcontainers import *
import datetime


class DCDTestCase(unittest.TestCase):

    # def test_AggregateDynamicNetwork(self):
    #     socioPatternsOriginalFile = "/Users/cazabetremy/ownCloud/Projets/SouaadNMI/SOCIOPATTERNdataset/thiers_2012.csv"
    #
    #     #load the file as a dynamic network
    #     dynNetwork = dn.readLinkStream(socioPatternsOriginalFile)
    #     dynNetwork = dynNetwork.aggregateTime(bin=60*60*24)
    #
    #     #write resulting file
    #     fileToWrite = "/Users/cazabetremy/ownCloud/Projets/SouaadNMI/SOCIOPATTERNdataset/SP2012.OMLRN"
    #     dn.writeAsOrderedModifList(dynNetwork,fileToWrite,dateEveryLine=True,nodeModifications=True)

    def test_runOLCPM(self):
        OLCPMlocation = "/Users/cazabetremy/ownCloud/Projets/SouaadNMI/SOCIOPATTERNdataset/OLCPM.jar"
        OMLRNfile = "/Users/cazabetremy/ownCloud/Projets/SouaadNMI/SOCIOPATTERNdataset/SP2012.OMLRN"
        directoryForOutput = "/Users/cazabetremy/ownCloud/Projets/SouaadNMI/SOCIOPATTERNdataset/test2"
        dn.launchCommandWaitAnswer("java -jar "+OLCPMlocation+ " -i "+OMLRNfile+" -o "+directoryForOutput+" -k 4",printOutput=False)

    # def test_Souaad(self):
    #
    #
    #     #Lire un fichier de vérité de terrain au format de SOCIOPATTERN
    #     groundTruthCommunities = dn.readStaticSNByNode("/Users/cazabetremy/Downloads/SOCIOPATTERNdataset/metadata_2012.txt")
    #
    #     #Définit une fonction qui transforme un nom de fichier en un identifiant de time step. (ici, extrait le timestamp du nom de fichier pour OLCPM)
    #     def fileNameToTimeID(fileName:str):
    #         if not fileName.startswith("Alv"):
    #             return None
    #         value = fileName[10:-6]
    #         return int(value)
    #
    #     #Charge des communautés dynamiques à partir d'un dossier qui contient 1 fichier par timestamp, avec les options pour lire les fichiers produits par OLCPM
    #     dynCom = dn.readSNByCom("/Users/cazabetremy/Downloads/SOCIOPATTERNdataset/test",fileNameToTimeID,nodeInBrackets=True,nodeSeparator=", ",nodeListPosition=2)
    #
    #     #Récupère les communautés
    #     communities = dynCom.communities()
    #
    #     #Pour chaque timestep, calcule la NMI entre les communautés à ce timestep et la ground truth
    #     NMIs = SortedDict()
    #     for t in communities:
    #         NMIs[t]=dn.NMI(set(communities[t].keys()),set(groundTruthCommunities.keys()))
    #
    #     #Affiche la liste des NMI calculées avec les dates/heures correspondantes
    #     for k,v in NMIs.items():
    #         print(datetime.datetime.fromtimestamp(k).strftime('%Y-%m-%d %H:%M:%S'),"\t",v)
    #




    # def test_print(self):
    #     dynG = dn.readSnapshotsDir("/Users/cazabetremy/Dropbox/dev/GOT/")
    #     durations = dynG.nodeLife()
    #     unfrequentNodes = [n for n in durations if len(durations[n]) <= 10]
    #     dynG.remove_nodes_from(unfrequentNodes)
    #     dn.writeAsOrderedModifList(dynG,"/Users/cazabetremy/Dropbox/GOT.OLCPM",True,True)


    # def test_DCDs(self):
    #     #Loading
    #     for i in range(50,550,50):
    #         #LFRtest = community.LFR_benchmark_graph(i,tau1=5,tau2=3,mu=0.2,average_degree=8.0,max_iters=100)
    #         SBMtest = nx.gaussian_random_partition_graph(i, 10, 10, .25, .1)
    #         dynG = dn.DynGraphSN()
    #         dynG.addSnaphsot(0,SBMtest)
    #
    #         timing1 = DCD.iLCD(dynG,runningTime=True)
    #
    #         for t in range(1,1000):
    #             previousGraph=dynG.snapshots(t-1).copy()
    #             nx.double_edge_swap(previousGraph)
    #             dynG.addSnaphsot(t, SBMtest)
    #
    #
    #
    #         #run tested algorithm
    #         timing2 = DCD.iLCD(dynG,runningTime=True)
    #
    #         print("size:,",i,",time:,",(timing2-timing1)/1000)



        #dn.show(coms, dynG)


    # def test_DCDs(self):
    #     #Loading
    #     dynG = dn.readSnapshotsDir("/Users/cazabetremy/Dropbox/dev/GOT/")
    #
    #     #Remove unfrequent nodes
    #     durations = dynG.nodeLife()
    #     unfrequentNodes = [n for n in durations if len(durations[n]) <= 10]
    #     dynG.remove_nodes_from(unfrequentNodes)
    #
    #     #aggregate some periods
    #     dynG.aggregate(10)
    #
    #     #run tested algorithm
    #     coms = DCD.iLCD(dynG)
    #     print(len(coms.communities))
    #     print(coms.communities)
    #     print(coms.nodes)
    #
    #     dn.show(coms, dynG)

if __name__ == '__main__':
    unittest.main()
