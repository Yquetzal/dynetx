from sortedcontainers import *

class intervals:
    """
    This class uses a sorted dictionary to maintain efficiently a proper interval

    """
    def __init__(self):

        self.interv  = SortedDict()


    def addInterval(self,interval):
        """

        :param interval: a tuple
        """
        #get the index of element that is just before the point where we should insert the provided interval
        toRemove=[]
        mergedInterv=interval
        iPotentialMergeLeft = self.interv.bisect_left(interval[0])-1
        if iPotentialMergeLeft!=-1: # if not first
            previousInterv = self.interv.peekitem(iPotentialMergeLeft)[1]
            if previousInterv[1]>=interval[0]:
                mergedInterv=self._mergeOverlappingIntervals(previousInterv,interval)
                toRemove.append(iPotentialMergeLeft)


        #get the index of element just after the end of the provided interval
        iPotentialMergeAfter = self.interv.bisect_left(interval[1])
        if iPotentialMergeAfter<len(self.interv):
            succInterv = self.interv.peekitem(iPotentialMergeAfter)[1]
            if succInterv[0]==mergedInterv[1] :
                mergedInterv = self._mergeOverlappingIntervals(mergedInterv, succInterv)
                toRemove.append(iPotentialMergeAfter)

        for i in range(iPotentialMergeLeft+1,iPotentialMergeAfter-1):
            toRemove.append(i)

        toRemove.sort()
        toRemove.reverse()
        for i in toRemove:
            del self.interv.iloc[i]
        self.interv[mergedInterv[0]]=mergedInterv



    def addIntervals(self,intervals): #inneficient if there is a lot of overlaps
        for interv in intervals:
            self.addInterval(interv)

    def getIntervals(self): #return a list of tuples
        return self.interv.values()

    def _mergeOverlappingIntervals(self,interval1,interval2):
        return ((min([interval1[0],interval2[0]]),max([interval1[1],interval2[1]])))

    def duration(self):
        totalDuration = 0
        for thisInterv in self.interv.values():
            totalDuration+=thisInterv[1]-thisInterv[0]
        return totalDuration

    def __str__(self):
        toReturn=""
        for interv in self.interv.values():
            toReturn+="["+str(interv[0])+","+str(interv[1])+"[ "
        return toReturn

    __repr__ = __str__