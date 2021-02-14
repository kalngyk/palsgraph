import palsgetpos
import numpy as np
import networkx as nx
from seaborn import color_palette

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
    node2idx = dict([(x, i) for (i, x) in enumerate(G.nodes)])
    clusters = []
    singletons = []
    for n, c in enumerate(communities):
        if len(c) == 1:
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
    color_map = []
    cls_elem_count = np.array([len(c) for c in communities])
    n2c = dict()
    for i, c in enumerate(communities):
        for n in c:
            n2c[str(n)] = i
    palette = color_palette(None, len(cls_elem_count[cls_elem_count > 1])+1)
    for node in G.nodes:
        c = n2c[node]
        if cls_elem_count[c] == 1:
            idx = len(palette) - 1
        else:
            idx = c % (len(palette) - 1)
        color_map.append(palette[idx])
    return color_map


