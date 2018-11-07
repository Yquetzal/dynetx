def nodes_com2node_com(community):
    node2com = dict()
    for nodes,id in community.items():
        for n in nodes:
            node2com[n]=id
    return node2com