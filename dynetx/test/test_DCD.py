import unittest
import dynetx as dn
import os
import dynetx.DCD as DCD


class DCDTestCase(unittest.TestCase):

    def test_DCDs(self):
        #Loading
        dynG = dn.readSnapshotsDir("/Users/cazabetremy/Dropbox/dev/GOT/")

        #Remove unfrequent nodes
        durations = dynG.nodeLife()
        unfrequentNodes = [n for n in durations if len(durations[n]) <= 10]
        dynG.remove_nodes_from(unfrequentNodes)

        #aggregate some periods
        dynG.aggregate(10)

        #run tested algorithm
        coms = DCD.muchaOriginal(dynG, om=0.3)

        dn.show(coms, dynG)

if __name__ == '__main__':
    unittest.main()
