from dynetx.utils import make_str
import dynetx as dn
from itertools import chain, count

__all__ = ['node_link_data', 'node_link_graph']
_attrs = dict(id='id', source='source', target='target')




def node_link_graph(data, directed=False, attrs=_attrs):
    """Return graph from node-link data format.

    Parameters
    ----------
    data : dict
        node-link formatted graph data

    directed : bool
        If True, and direction not specified in data, return a directed graph.

    attrs : dict
        A dictionary that contains three keys 'id', 'source', 'target'.
        The corresponding values provide the attribute names for storing
        Dynetx-internal graph data. Default value:
        :samp:`dict(id='id', source='source', target='target')`.

    Returns
    -------
    G : DyNetx graph
       A DyNetx graph object

    Examples
    --------
    >>> from dynetx.readwrite import json_graph
    >>> G = dn.DynGraphTN([(1,2)])
    >>> data = json_graph.node_link_data(G)
    >>> H = json_graph.node_link_graph(data)

    See Also
    --------
    node_link_data
    """

    directed = data.get('directed', directed)
    graph = dn.DynGraphTN()
    if directed:
        graph = graph.to_directed()

    id_ = attrs['id']
    mapping = []
    graph.graph = data.get('graph', {})
    c = count()
    for d in data['nodes']:
        node = d.get(id_, next(c))
        mapping.append(node)
        nodedata = dict((make_str(k), v) for k, v in d.items() if k != id_)
        graph.add_node(node, **nodedata)
    for d in data['links']:
        graph.add_interaction(d['source'], d["target"], d['time'])

    return graph
