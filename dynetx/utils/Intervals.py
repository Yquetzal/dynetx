from sortedcontainers import *

class intervals:
    """
    This class uses a sorted dictionary to maintain efficiently a proper interval

    """
    def __init__(self):

        self.interv  = SortedDict()

    def containsT(self,t):
        iBefore = self.interv.bisect_right(t) - 1
        if iBefore >= 0:
            potentialInterval = self.interv.peekitem(iBefore)
            print(potentialInterval)
            if potentialInterval[1][0] <= t < potentialInterval[1][1]:
                return True
        return False

    def addInterval(self,interval):
        """

        :param interval: a tuple
        """
        #get the index of element that is just before the point where we should insert the provided interval
        toRemove=[]
        mergedInterv=interval
        iPotentialMergeLeft = self.interv.bisect_left(interval[0])-1
        if iPotentialMergeLeft!=-1: # if not inserted at the beginning
            previousInterv = self.interv.peekitem(iPotentialMergeLeft)[1]
            if previousInterv[1]>=interval[0]: #if previous interval end after beggining of new
                mergedInterv=self._mergeOverlappingIntervals(previousInterv,interval) #merge
                toRemove.append(iPotentialMergeLeft) #delete previous


        #get the index of element just before (or exactly at) the end of the provided interval
        iPotentialMergeAfter = self.interv.bisect_left(interval[1])

        if iPotentialMergeAfter<len(self.interv): #if new interval not ending after last
            succInterv = self.interv.peekitem(iPotentialMergeAfter)[1]
            if succInterv[0]==mergedInterv[1] : #if start of element = end of new element
                mergedInterv = self._mergeOverlappingIntervals(mergedInterv, succInterv) #merge them
                toRemove.append(iPotentialMergeAfter)

        for i in range(iPotentialMergeLeft+1,iPotentialMergeAfter):
            toRemove.append(i)

        toRemove.sort()
        toRemove.reverse()
        for i in toRemove:
            del self.interv.iloc[i]
        self.interv[mergedInterv[0]]=mergedInterv

    def removeInterval(self,interval):

        # get the index of element that is just before the interval we want to remove
        toRemove = []
        toAdd=[]
        iMinToDelete = self.interv.bisect_left(interval[0])-1
        iMaxToDelete = self.interv.bisect_left(interval[1])

        for i in range(max(0,iMinToDelete),iMaxToDelete):
            toRemove.append(i)
            afterSubstraction = self._substractIntervals(self.interv.peekitem(i)[1],interval)

            for interv in  afterSubstraction:
                if interv!=[]:
                    toAdd.append(interv)

        toRemove.sort()
        toRemove.reverse()
        for i in toRemove:
            del self.interv.iloc[i]
        for newIntervs in toAdd:
            self.interv[newIntervs[0]] = newIntervs


    def addIntervals(self,intervals): #inneficient if there is a lot of overlaps
        for interv in intervals:
            self.addInterval(interv)

    def getIntervals(self): #return a list of tuples
        return list(self.interv.values())

    def _mergeOverlappingIntervals(self,interval1,interval2):
        return ((min([interval1[0],interval2[0]]),max([interval1[1],interval2[1]])))

    def _substractIntervals(self,before,toSubstract):
        left=[]
        right=[]
        if toSubstract[0]>before[0]:
            left=(before[0],min(before[1],toSubstract[0]))

        if toSubstract[1]<before[1]:
            right=(max(toSubstract[1],before[0]),before[1])
        return(left,right)

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