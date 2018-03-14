from __future__ import absolute_import
import unittest
import dynetx as dn
import os
from dynetx.utils.Intervals import intervals
import numpy as np


class ReadWriteTestCase(unittest.TestCase):

    def test_oneInterval(self):
        anInt = intervals()
        anInt.addInterval((2,3))
        results = anInt.getIntervals()
        self.assertEqual(results,[(2,3)])

    def test_addingIntervals(self):
        anInt = intervals()
        anInt.addInterval((2,3))
        anInt.addInterval((5, 7))
        results = anInt.getIntervals()
        self.assertEqual(results,[(2,3),(5,7)])

    def test_addingOverlappingIntervals(self):
        anInt = intervals()
        anInt.addInterval((2,3))
        anInt.addInterval((2, 5))
        results = anInt.getIntervals()
        self.assertEqual(results,[(2,5)])

    def test_addingOverlappingIntervals2(self):
        anInt = intervals()
        anInt.addInterval((2,3))
        anInt.addInterval((0, 5))
        results = anInt.getIntervals()
        self.assertEqual(results,[(0,5)])

    def test_addingIntervalsComplex(self):
        anInt = intervals()
        anInt.addInterval((2, 3))

        anInt.addInterval((5, 6))
        self.assertEqual(anInt.getIntervals(), [(2, 3),(5,6)])

        anInt.addInterval((6, 10))
        self.assertEqual(anInt.getIntervals(), [(2, 3),(5,10)])

        anInt.addInterval((20, 100))
        self.assertEqual(anInt.getIntervals(), [(2, 3),(5,10),(20,100)])

        anInt.addInterval((101, 201))
        self.assertEqual(anInt.getIntervals(), [(2, 3),(5,10),(20,100),(101,201)])

        anInt.addInterval((100, 101))
        self.assertEqual(anInt.getIntervals(), [(2, 3),(5,10),(20,201)])

        anInt.addInterval((3, 300))
        self.assertEqual(anInt.getIntervals(), [(2, 300)])

    def test_delete(self):
        anInt = intervals()
        anInt.addInterval((10, 100))

        anInt.removeInterval((20, 30))
        self.assertEqual(anInt.getIntervals(), [(10,20),(30,100)])

    def test_delete2(self):
        anInt = intervals()
        anInt.addInterval((10, 100))
        anInt.addInterval((200, 300))

        anInt.removeInterval((0, 5))
        anInt.removeInterval((150, 160))
        anInt.removeInterval((350, 450))

        self.assertEqual(anInt.getIntervals(), [(10, 100),(200,300)])

    def test_deleteComplete(self):
        anInt = intervals()
        anInt.addInterval((10, 100))
        anInt.addInterval((200, 300))

        anInt.removeInterval((5, 15))
        self.assertEqual([(15, 100),(200,300)],anInt.getIntervals())

        anInt.removeInterval((20, 30))
        self.assertEqual([(15, 20),(30,100),(200,300)],anInt.getIntervals() )

        anInt.removeInterval((0,300))
        self.assertEqual([],anInt.getIntervals() )

    def test_inf(self):
        print("--------------------")

        anInt = intervals()
        anInt.addInterval((10, np.inf))
        anInt.addInterval((20, np.inf))
        self.assertEqual([(10, np.inf)],anInt.getIntervals())
        anInt.removeInterval((20,np.inf))
        self.assertEqual([(10, 20)],anInt.getIntervals())




if __name__ == '__main__':
    unittest.main()
