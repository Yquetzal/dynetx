"""Base class for undirected dynamic graphs.

The DynGraph class allows any hashable object as a node.
Of each interaction needs be specified the set of timestamps of its presence.

Self-loops are allowed.
"""

import networkx as nx
from collections import defaultdict
from dynetx.utils import not_implemented
from copy import deepcopy
from dynetx.utils import *
import math

__author__ = 'Giulio Rossetti'
__license__ = "GPL"
__email__ = "giulio.rossetti@gmail.com"


class DynGraphTN(nx.Graph):


    def __init__(self, data=None, edge_removal=True, **attr):

        super(self.__class__, self).__init__(data, **attr)
        #self.time_to_edge = defaultdict(int)
        self.start=math.inf
        self.end=-math.inf

    def nodesD(self,nbunch=None,t=None):
        if t!=None:
            raise Exception("not implemented yet")
        return self.nodeLife(nbunch)

    def edgesD(self,nbunch=None):
        toReturn = {}
        if nbunch != None:
            nbunch = "not implemented yet"
        for (n1,n2, data) in self.edges(data=True):
            toReturn[(n1,n2)]=data["t"]
        return toReturn


    def add_interaction(self, u, v, t=None, e=None):

        if t is None:
            raise nx.NetworkXError(
                "The t argument must be specified.")

        if not self.has_node(u):
            self.add_node(u,t,e)
        if not self.has_node(v):
            self.add_node(v,t,e)

        if not self.has_edge(u,v):
            self._add_edge(u,v,t=intervals())
        self[u][v]["t"].addInterval((t,e))

        self.start = min(self.start,t)
        self.end = max(self.end, e)

    def add_interactions_from(self, ebunch, t=None, e=None):
        # set up attribute dict
        if t is None:
            raise nx.NetworkXError(
                "The t argument must be a specified.")
        # process ebunch
        for ed in ebunch:
            self.add_interaction(ed[0], ed[1], t, e)



    def number_of_nodes(self, t=None):
        if t is None:
            return len(self.node)
        else:
            nds = sum([1 for n in self.degree(t=t).values() if n > 0])
            return nds


    def has_node(self, n, t=None):

        if t is None:
            try:
                return n in self.node
            except TypeError:
                return False
        else:
            deg = list(self.degree([n], t).values())
            if len(deg) > 0:
                return deg[0] > 0
            else:
                return False


    def time_slice(self, t_from, t_to=None):
        # create new graph and copy subgraph into it
        H = self.__class__()

        if t_to is not None:
            if t_to < t_from:
                raise ValueError("Invalid range: t_to must be grater that t_from")
        else:
            t_to = t_from

        for u, v, ts in self.interactions_iter():
            t_to_cp = t_to
            t_from_cp = t_from

            for r in ts['t']:
                if t_to < r[0]:
                    break

                if t_from < r[0] < t_to or t_to >= r[1]:
                    t_from_cp = r[0]
                    t_to_cp = t_to
                if r[0] <= t_from_cp <= r[1]:
                    if t_to_cp is None:
                        H.add_interaction(u, v, t_from_cp)
                    else:
                        if t_from_cp < t_to_cp <= r[1]:
                            H.add_interaction(u, v, t_from_cp, t_to_cp+1)
                        else:
                            H.add_interaction(u, v, t_from_cp, r[1]+1)
                            t_to_cp = r[1]
        return H


    @not_implemented()
    def remove_edge(self, u, v):
        pass

    @not_implemented()
    def remove_edges_from(self, ebunch):
        pass

    @not_implemented()
    def remove_node(self, u):
        pass

    @not_implemented()
    def remove_nodes_from(self, nbunch):
        pass

    def add_edge(self, u, v, t,e, attr_dict=None, **attr):
        self.add_interaction(u,v,t,e)


    def _add_edge(self, u, v, attr_dict=None, **attr):
        super(DynGraphTN,self).add_edge(u,v,attr_dict=None, **attr)

    def add_edges_from(self, ebunch, attr_dict=None, **attr):
        for (u,v,t,e) in ebunch:
            self.add_edge(u,v,t,e)


    def _add_node(self, u, attr_dict=None, **attr):
        super(DynGraphTN,self).add_node(u,attr_dict=None, **attr)

    def _nodes(self,data=False):
        return super(DynGraphTN, self).nodes(data=data)

    def _edges(self, data=False):
        return super(DynGraphTN, self).edges(data=data)

    def add_node(self,n,t,e):
        if not self.has_node(n):
            self._add_node(n,t=intervals())
        self.node[n]["t"].addInterval((t,e))

    def add_nodes_from(self,nodes):
        for (n,t,e) in nodes:
            self.add_node(n,t,e)

    def nodeLife(self, nbunch=None):  # return a dictionary, for each node its existing times
        toReturn = {} #type:{str:[intervals]}
        if nbunch != None:
            nbunch = "not implemented yet"
        for (n,data) in self.nodes(data=True):
            toReturn[n]=data["t"]
        return toReturn