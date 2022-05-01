import palsgetpos
import numpy as np
import networkx as nx
from seaborn import color_palette
from colorcet import glasbey

__all__ = ['make_graph', 'getpos', 'gen_colormap']


def make_graph(dist, labels=None, show_singletons=False):
    if dist.shape[0] != dist.shape[1]:
        print("Error: distance matrix must be symmetric")
        return None
    G = nx.Graph()
    for (i, j) in [(i, j) for i in range(dist.shape[0]) for j in range(dist.shape[1]) if i != j and dist[i,j] != 0]:
        if labels == None:
            G.add_edge(i, j, weight=dist[i,j])
        else:
            if show_singletons:
                G.add_nodes_from(labels)
            G.add_edge(labels[i], labels[j], weight=dist[i,j])
    return G


def getpos(G, communities):
    """
    Find a position for every node in G.nodes according to the clusters specified in communities
    Every name in communities must exist in G.nodes, but not every node in G.nodes needs to be
    in communities.

    :param G: A NetworkX graph
    :param communities: A list of lists
    :return: An list of the same length of G.nodes. Each element in the list is a position for a node.
    """
    elems = [item for sublist in communities for item in sublist]
    for node in G.nodes:
        if node not in elems: 
            raise Exception("Exists node in G not specified in communities") 

    node2idx = dict([(x, i) for (i, x) in enumerate(G.nodes)])
    clusters = []
    singletons = []
    for n, c in enumerate(communities):
        if len(c) == 1:
            if c[0] in G.nodes:
                singletons.extend([node2idx[x] for x in c])
        indices = [node2idx[x] for x in G.nodes if x in c]
        for i in indices:
            clusters.append([i, n])
    clusters = np.array(clusters)
    edges = [[node2idx[x], node2idx[y]] for x, y in G.edges]
    edges.extend([[x, x] for x in singletons])
    edges = np.array(edges)
    pos = palsgetpos.getpos(edges, clusters)
    nodes = np.array(G.nodes)
    results = dict([(nodes[int(i)], np.array([j, k])) for i, j, k in pos])
    return results


def gen_colormap(G, communities):
    """
    Generate a color for every node in G.nodes. Nodes in the same community according to communities
    are given the same color.
    Every name in communities must exist in G.nodes, but not every node in G.nodes needs to be in
    communities.

    :param G: A NetworkX graph
    :param communities: A list of lists
    :return: An list of the same length of G.nodes. Each element in the list is a color for a node.
    """
    elems = [item for sublist in communities for item in sublist]
    for node in G.nodes:
        if node not in elems: 
            raise Exception("Exists node in G not specified in communities") 

    color_map = []
    n2c = dict()
    color_count = 0
    for c in communities:
        if len(c) > 1:
            for n in c:
                n2c[str(n)] = color_count
            color_count += 1
        else:
            for n in c:
                n2c[str(n)] = -1
    palette = color_palette(glasbey, color_count + 1)
    for node in G.nodes:
        idx = n2c[str(node)] if n2c[str(node)] >= 0 else color_count 
        color_map.append(palette[idx])
    return color_map

