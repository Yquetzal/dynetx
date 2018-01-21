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
    """
    Base class for undirected dynamic graphs.

    A DynGraph stores nodes and timestamped interaction.

    DynGraph hold undirected interaction.  Self loops are allowed.

    Nodes can be arbitrary (hashable) Python objects with optional
    key/value attributes.

    Parameters
    ----------
    data : input graph
        Data to initialize graph.  If data=None (default) an empty
        graph is created.  The data can be an interaction list, or any
        NetworkX graph object.

    attr : keyword arguments, optional (default= no attributes)
        Attributes to add to graph as key=value pairs.

    edge_removal : bool, optional (default=True)
        Specify if the dynamic graph instance should allows edge removal or not.

    See Also
    --------
    DynDiGraph

    Examples
    --------
    Create an empty graph structure (a "null graph") with no nodes and
    no interactions.

    >>> G = dn.DynGraph()

    G can be grown in several ways.

    **Nodes:**

    Add one node at a time:

    >>> G.add_node(1)

    Add the nodes from any container (a list, dict, set or
    even the lines from a file or the nodes from another graph).

    >>> G.add_nodes_from([2,3])
    >>> G.add_nodes_from(range(100,110))
    >>> H=dn.DynGraph()
    >>> H.add_path([0,1,2,3,4,5,6,7,8,9], t=0)
    >>> G.add_nodes_from(H)

    In addition to strings and integers any hashable Python object
    (except None) can represent a node.

    >>> G.add_node(H)

    **Edges:**

    G can also be grown by adding interaction and specifying their timestamp.

    Add one interaction,

    >>> G.add_interaction(1, 2, t=0)

    a list of interaction

    >>> G.add_interactions_from([(3, 2), (1,3)], t=1)

    If some interaction connect nodes not yet in the graph, the nodes
    are added automatically.

    To traverse all interactions of a graph a time t use the interactions(t) method.

    >>> G.interactions(t=1)
    [(3, 2), (1, 3)]
    """

    def __init__(self, data=None, edge_removal=True, **attr):
        """Initialize a graph with interaction, name, graph attributes.

        Parameters
        ----------
        data : input graph
            Data to initialize graph.  If data=None (default) an empty
            graph is created.  The data can be an interaction list, or any
            NetworkX/DyNetx graph object.  If the corresponding optional Python
            packages are installed the data can also be a NumPy matrix
            or 2d ndarray, a SciPy sparse matrix, or a PyGraphviz graph.
        edge_removal : bool, optional (default=True)
            Specify if the dynamic graph instance should allows edge removal or not.
        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G = dn.DynGraph(edge_removal=True)
        """
        super(self.__class__, self).__init__(data, **attr)
        self.time_to_edge = defaultdict(int)
        self.start=math.inf
        self.end=-math.inf

    def nodesD(self, t=None,data=False):
        """Return an iterator over the nodes with respect to a given temporal snapshot.

        Parameters
        ----------
        t : snapshot id (default=None).
            If None the iterator returns all the nodes of the flattened graph.
        data : boolean, optional (default=False)
               If False the iterator returns nodes.  If True
               return a two-tuple of node and node data dictionary

        Returns
        -------
        niter : iterator
            An iterator over nodes.  If data=True the iterator gives
            two-tuples containing (node, node data, dictionary)

        Examples
        --------
        >>> G = dn.DynGraph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_path([0,1,2], 0)

        >>> [n for n, d in G.nodes_iter(t=0)]
        [0, 1, 2]
        """
        return iter([(n,d["t"]) for (n,d) in self._nodes(data=True)])

    def edges(self,data=False):
        return iter([(u,v,d["t"]) for (u,v,d) in self._edges(data=True)])

    def __presence_test(self, u, v, t):
        spans = self._adj[u][v]['t']
        if self.edge_removal:
            if spans[0][0] <= t <= spans[-1][1]:
                for s in spans:
                    if t in range(s[0], s[1]+1):
                        return True
        else:
            if spans[0][0] <= t <= max(self.temporal_snapshots_ids()):
                return True

        return False

    def interactions(self, nbunch=None, t=None):
        """Return an iterator over the interaction present in a given snapshot.

        Edges are returned as tuples
        in the order (node, neighbor).

        Parameters
        ----------
        nbunch : iterable container, optional (default= all nodes)
            A container of nodes.  The container will be iterated
            through once.
        t : snapshot id (default=None)
            If None the the method returns an iterator over the edges of the flattened graph.

        Returns
        -------
        edge_iter : iterator
            An iterator of (u,v) tuples of interaction.

        See Also
        --------
        interaction : return a list of interaction

        Notes
        -----
        Nodes in nbunch that are not in the graph will be (quietly) ignored.
        For directed graphs this returns the out-interaction.

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2], 0)
        >>> G.add_interaction(2,3,1)
        >>> [e for e in G.interactions_iter(t=0)]
        [(0, 1), (1, 2)]
        >>> list(G.interactions_iter())
        [(0, 1), (1, 2), (2, 3)]
        """
        seen = {}  # helper dict to keep track of multiply stored interactions
        if nbunch is None:
            nodes_nbrs = self._adj.items()
        else:
            nodes_nbrs = ((n, self._adj[n]) for n in self.nbunch_iter(nbunch))

        for n, nbrs in nodes_nbrs:
            for nbr in nbrs:
                if t is not None:
                    if nbr not in seen and self.__presence_test(n, nbr, t):
                        yield (n, nbr, {"t": [t]})
                else:
                    if nbr not in seen:
                        yield (n, nbr, self._adj[n][nbr])
                seen[n] = 1
        del seen

    def add_interaction(self, u, v, t=None, e=None):
        """Add an interaction between u and v at time t vanishing (optional) at time e.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Parameters
        ----------
        u, v : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        t : appearance snapshot id, mandatory
        e : vanishing snapshot id, optional (default=None)

        See Also
        --------
        add_edges_from : add a collection of interaction at time t

        Notes
        -----
        Adding an interaction that already exists but with different snapshot id updates the interaction data.

        Examples
        --------
        The following all add the interaction e=(1,2, 0) to graph G:

        >>> G = dn.DynGraph()
        >>> G.add_interaction(1, 2, 0)           # explicit two-node form
        >>> G.add_interaction( [(1,2)], t=0 ) # add interaction from iterable container

        Specify the vanishing of the interaction

        >>>> G.add_interaction(1, 3, t=1, e=10)

        will produce an interaction present in snapshots [0, 9]
        """
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
        """Add all the interaction in ebunch at time t.

        Parameters
        ----------
        ebunch : container of interaction
            Each interaction given in the container will be added to the
            graph. The interaction must be given as as 2-tuples (u,v) or
            3-tuples (u,v,d) where d is a dictionary containing interaction
            data.
        t : appearance snapshot id, mandatory
        e : vanishing snapshot id, optional

        See Also
        --------
        add_edge : add a single interaction

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_edges_from([(0,1),(1,2)], t=0)
        """
        # set up attribute dict
        if t is None:
            raise nx.NetworkXError(
                "The t argument must be a specified.")
        # process ebunch
        for ed in ebunch:
            self.add_interaction(ed[0], ed[1], t, e)

    def number_of_interactions(self, u=None, v=None, t=None):
        """Return the number of interaction between two nodes at time t.

        Parameters
        ----------
        u, v : nodes, optional (default=all interaction)
            If u and v are specified, return the number of interaction between
            u and v. Otherwise return the total number of all interaction.
        t : snapshot id (default=None)
            If None will be returned the number of edges on the flattened graph.


        Returns
        -------
        nedges : int
            The number of interaction in the graph.  If nodes u and v are specified
            return the number of interaction between those nodes. If a single node is specified return None.

        See Also
        --------
        size

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> G.number_of_interactions()
        3
        >>> G.number_of_interactions(0,1, t=0)
        1
        >>> G.add_edge(3, 4, t=1)
        >>> G.number_of_interactions()
        4
        """
        if t is None:
            if u is None:
                return int(self.size())
            elif u is not None and v is not None:
                if v in self._adj[u]:
                    return 1
                else:
                    return 0
        else:
            if u is None:
                return int(self.size(t))
            elif u is not None and v is not None:
                if v in self._adj[u]:
                    if self.__presence_test(u, v, t):
                        return 1
                    else:
                        return 0

    def has_interaction(self, u, v, t=None):
        """Return True if the interaction (u,v) is in the graph at time t.

        Parameters
        ----------
        u, v : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        t : snapshot id (default=None)
            If None will be returned the presence of the interaction on the flattened graph.


        Returns
        -------
        edge_ind : bool
            True if interaction is in the graph, False otherwise.

        Examples
        --------
        Can be called either using two nodes u,v or interaction tuple (u,v)

        >>> G = nx.Graph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> G.has_interaction(0,1, t=0)
        True
        >>> G.has_interaction(0,1, t=1)
        False
        """
        try:
            if t is None:
                return v in self._adj[u]
            else:
                return v in self._adj[u] and self.__presence_test(u, v, t)
        except KeyError:
            return False

    def neighbors(self, n, t=None):
        """Return a list of the nodes connected to the node n at time t.

        Parameters
        ----------
        n : node
           A node in the graph
        t : snapshot id (default=None)
            If None will be returned the neighbors of the node on the flattened graph.


        Returns
        -------
        nlist : list
            A list of nodes that are adjacent to n.

        Raises
        ------
        NetworkXError
            If the node n is not in the graph.

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> G.neighbors(0, t=0)
        [1]
        >>> G.neighbors(0, t=1)
        []
        """
        try:
            if t is None:
                return list(self._adj[n])
            else:
                return [i for i in self._adj[n] if self.__presence_test(n, i, t)]
        except KeyError:
            raise nx.NetworkXError("The node %s is not in the graph." % (n,))

    def neighbors_iter(self, n, t=None):
        """Return an iterator over all neighbors of node n at time t.

        Parameters
        ----------
        n : node
           A node in the graph
        t : snapshot id (default=None)
            If None will be returned an iterator over the neighbors of the node on the flattened graph.

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> [n for n in G.neighbors_iter(0, t=0)]
        [1]
        """
        try:
            if t is None:
                return iter(self._adj[n])
            else:
                return iter([i for i in self._adj[n] if self.__presence_test(n, i, t)])
        except KeyError:
            raise nx.NetworkXError("The node %s is not in the graph." % (n,))


    def degree(self, nbunch=None, t=None):
        """Return an iterator for (node, degree) at time t.

        The node degree is the number of edges adjacent to the node in a given timeframe.

        Parameters
        ----------
        nbunch : iterable container, optional (default=all nodes)
            A container of nodes.  The container will be iterated
            through once.

        t : snapshot id (default=None)
            If None will be returned an iterator over the degree of nodes on the flattened graph.


        Returns
        -------
        nd_iter : an iterator
            The iterator returns two-tuples of (node, degree).

        See Also
        --------
        degree

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> list(G.degree_iter(0, t=0))
        [(0, 1)]
        >>> list(G.degree_iter([0,1], t=0))
        [(0, 1), (1, 2)]
        """
        if nbunch is None:
            nodes_nbrs = self._adj.items()
        else:
            nodes_nbrs = ((n, self._adj[n]) for n in self.nbunch_iter(nbunch))

        if t is None:
            for n, nbrs in nodes_nbrs:
                deg = len(self._adj[n])
                yield (n, deg)
        else:
            for n, nbrs in nodes_nbrs:
                edges_t = len([v for v in nbrs.keys() if self.__presence_test(n, v, t)])
                if edges_t > 0:
                    yield (n, edges_t)
                else:
                    yield (n, 0)

    def size(self, t=None):
        """Return the number of edges at time t.

        Parameters
        ----------
        t : snapshot id (default=None)
            If None will be returned the size of the flattened graph.


        Returns
        -------
        nedges : int
            The number of edges

        See Also
        --------
        number_of_edges

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> G.size(t=0)
        3
        """
        s = sum(self.degree(t=t).values()) / 2
        return int(s)

    def number_of_nodes(self, t=None):
        """Return the number of nodes in the t snpashot of a dynamic graph.

        Parameters
        ----------
        t : snapshot id (default=None)
               If None return the number of nodes in the flattened graph.


        Returns
        -------
        nnodes : int
            The number of nodes in the graph.

        See Also
        --------
        order  which is identical

        Examples
        --------
        >>> G = dn.DynGraph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_path([0,1,2], t=0)
        >>> G.number_of_nodes(0)
        3
        """
        if t is None:
            return len(self._node)
        else:
            nds = sum([1 for n in self.degree(t=t).values() if n > 0])
            return nds

    def order(self, t=None):
        """Return the number of nodes in the t snpashot of a dynamic graph.

        Parameters
        ----------
        t : snapshot id (default=None)
               If None return the number of nodes in the flattened graph.


        Returns
        -------
        nnodes : int
            The number of nodes in the graph.

        See Also
        --------
        number_of_nodes  which is identical

        Examples
        --------
        >>> G = dn.DynGraph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_path([0,1,2], t=0)
        >>> G.order(0)
        3
        """
        return self.number_of_nodes(t)

    def has_node(self, n, t=None):
        """Return True if the graph, at time t, contains the node n.

        Parameters
        ----------
        n : node
        t : snapshot id (default None)
                If None return the presence of the node in the flattened graph.

        Examples
        --------
        >>> G = dn.DynGraph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_path([0,1,2], t=0)
        >>> G.has_node(0, t=0)
        True

        It is more readable and simpler to use

        >>> 0 in G
        True

        """
        if t is None:
            try:
                return n in self._node
            except TypeError:
                return False
        else:
            deg = list(self.degree([n], t).values())
            if len(deg) > 0:
                return deg[0] > 0
            else:
                return False

    def add_star(self, nodes, t=None):
        """Add a star at time t.

        The first node in nodes is the middle of the star.  It is connected
        to all other nodes.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes.
        t : snapshot id (default=None)

        See Also
        --------
        add_path, add_cycle

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_star([0,1,2,3], t=0)
        """
        nlist = list(nodes)
        v = nlist[0]
        interaction = ((v, n) for n in nlist[1:])
        self.add_interactions_from(interaction, t)

    def add_path(self, nodes, t=None):
        """Add a path at time t.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes.
        t : snapshot id (default=None)

        See Also
        --------
        add_path, add_cycle

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        """
        nlist = list(nodes)
        interaction = zip(nlist[:-1], nlist[1:])
        self.add_interactions_from(interaction, t)

    def add_cycle(self, nodes, t=None):
        """Add a cycle at time t.

        Parameters
        ----------
        nodes : iterable container
            A container of nodes.
        t : snapshot id (default=None)

        See Also
        --------
        add_path, add_cycle

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_cycle([0,1,2,3], t=0)
        """
        nlist = list(nodes)
        interaction = zip(nlist, nlist[1:] + [nlist[0]])
        self.add_interactions_from(interaction, t)

    def to_directed(self):
        """Return a directed representation of the graph.

        Returns
        -------
        G : DynDiGraph
            A dynamic directed graph with the same name, same nodes, and with
            each edge (u,v,data) replaced by two directed edges
            (u,v,data) and (v,u,data).

        Notes
        -----
        This returns a "deepcopy" of the edge, node, and
        graph attributes which attempts to completely copy
        all of the data and references.

        This is in contrast to the similar D=DynDiGraph(G) which returns a
        shallow copy of the data.

        See the Python copy module for more information on shallow
        and deep copies, http://docs.python.org/library/copy.html.

        Warning: If you have subclassed Graph to use dict-like objects in the
        data structure, those changes do not transfer to the DynDiGraph
        created by this method.

        Examples
        --------
        >>> G = dn.DynGraph()   # or MultiGraph, etc
        >>> G.add_path([0,1])
        >>> H = G.to_directed()
        >>> H.edges()
        [(0, 1), (1, 0)]

        If already directed, return a (deep) copy

        >>> G = dn.DynDiGraph()   # or MultiDiGraph, etc
        >>> G.add_path([0,1])
        >>> H = G.to_directed()
        >>> H.edges()
        [(0, 1)]
        """
        from .dyndigraph import DynDiGraph
        G = DynDiGraph()
        G.name = self.name
        G.add_nodes_from(self)
        for it in self.interactions_iter():
            for t in it[2]['t']:
                G.add_interaction(it[0], it[1], t=t[0], e=t[1])

        G.graph = deepcopy(self.graph)
        G._node = deepcopy(self._node)
        return G

    def stream_interactions(self):
        """Generate a temporal ordered stream of interactions.


        Returns
        -------
        nd_iter : an iterator
            The iterator returns a 4-tuples of (node, node, op, timestamp).

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> G.add_path([3,4,5,6], t=1)
        >>> list(G.stream_interactions())
        [(0, 1, '+', 0), (1, 2, '+', 0), (2, 3, '+', 0), (3, 4, '+', 1), (4, 5, '+', 1), (5, 6, '+', 1)]
        """
        timestamps = sorted(self.time_to_edge.keys())
        for t in timestamps:
            for e in self.time_to_edge[t]:
                yield (e[0], e[1], e[2], t)

    def time_slice(self, t_from, t_to=None):
        """Return an new graph containing nodes and interactions present in [t_from, t_to].

            Parameters
            ----------

            t_from : snapshot id, mandatory
            t_to : snapshot id, optional (default=None)
                If None t_to will be set equal to t_from

            Returns
            -------
            H : a DynGraph object
                the graph described by interactions in [t_from, t_to]

            Examples
            --------
            >>> G = dn.DynGraph()
            >>> G.add_path([0,1,2,3], t=0)
            >>> G.add_path([0,4,5,6], t=1)
            >>> G.add_path([7,1,2,3], t=2)
            >>> H = G.time_slice(0)
            >>> H.interactions()
            [(0, 1), (1, 2), (1, 3)]
            >>> H = G.time_slice(0, 1)
            >>> H.interactions()
            [(0, 1), (1, 2), (1, 3), (0, 4), (4, 5), (5, 6)]
        """
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

    def temporal_snapshots_ids(self):
        """Return the ordered list of snapshot ids present in the dynamic graph.

            Returns
            -------

            nd : list
                a list of snapshot ids

            Examples
            --------
            >>> G = dn.DynGraph()
            >>> G.add_path([0,1,2,3], t=0)
            >>> G.add_path([0,4,5,6], t=1)
            >>> G.add_path([7,1,2,3], t=2)
            >>> G.temporal_snapshots_ids()
            [0, 1, 2]
        """
        return sorted(self.snapshots.keys())

    def interactions_per_snapshots(self, t=None):
        """Return the number of interactions within snapshot t.

        Parameters
        ----------

        t : snapshot id (default=None)
            If None will be returned total number of interactions across all snapshots

        Returns
        -------

        nd : dictionary, or number
            A dictionary with snapshot ids as keys and interaction count as values or
            a number if a single snapshot id is specified.

        Examples
        --------
        >>> G = dn.DynGraph()
        >>> G.add_path([0,1,2,3], t=0)
        >>> G.add_path([0,4,5,6], t=1)
        >>> G.add_path([7,1,2,3], t=2)
        >>> G.interactions_per_snapshots(t=0)
        3
        >>> G.interactions_per_snapshots()
        {0: 3, 1: 3, 2: 3}
        """
        if t is None:
            return {k: v/2 for k, v in self.snapshots.items()}
        else:
            try:
                return self.snapshots[t]/2
            except KeyError:
                return 0

    def inter_event_time_distribution(self, u=None, v=None):
        """Return the distribution of inter event time.
        If u and v are None the dynamic graph intere event distribution is returned.
        If u is specified the inter event time distribution of interactions involving u is returned.
        If u and v are specified the inter event time distribution of (u, v) interactions is returned

        Parameters
        ----------

        u : node id
        v : node id

        Returns
        -------

        nd : dictionary
            A dictionary from inter event time to number of occurrences

        """
        dist = {}
        if u is None:
            # global inter event
            first = True
            delta = None
            for ext in self.stream_interactions():
                if first:
                    delta = ext
                    first = False
                    continue
                disp = ext[-1] - delta[-1]
                delta = ext
                if disp in dist:
                    dist[disp] += 1
                else:
                    dist[disp] = 1

        elif u is not None and v is None:
            # node inter event
            delta = (0, 0, 0, 0)
            flag = False
            for ext in self.stream_interactions():
                if ext[0] == u or ext[1] == u:
                    if flag:
                        disp = ext[-1] - delta[-1]
                        delta = ext
                        if disp in dist:
                            dist[disp] += 1
                        else:
                            dist[disp] = 1
                    else:
                        delta = ext
                        flag = True
        else:
            # interaction inter event
            evt = self._adj[u][v]['t']
            delta = []

            for i in evt:
                if i[0] != i[1]:
                    for j in [0, 1]:
                        delta.append(i[j])
                else:
                    delta.append(i[0])

            if len(delta) == 2 and delta[0] == delta[1]:
                return {}

            for i in range(0, len(delta) - 1):
                e = delta[i + 1] - delta[i]
                if e not in dist:
                    dist[e] = 1
                else:
                    dist[e] += 1

        return dist

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

