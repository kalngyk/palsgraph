import matplotlib
matplotlib.use('pdf')
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform
import palsgraph
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman
from itertools import islice

#####################################################################################
# Load matrix

simfilename = 'test.tsv'
X = np.genfromtxt(simfilename, delimiter='\t', encoding='utf8', dtype=None)

# Get labels in the order that they appear in the file
labels = []
for label in [x[0] for x in X]:
    if label in labels:
        continue
    labels.append(label)
for label in [x[1] for x in X]:
    if label in labels:
        continue
    labels.append(label)

dismat = squareform([x[2] for x in X])

#####################################################################################
# Constructs graph from distance matrix

threshold = 0.77 # Replace this with your choice of threshold

# Initialize similarity matrix
simmat = dismat.copy().reshape((-1,))

# Preparation: remember the indices of the disconnected entries
unconnected_indices = (simmat > threshold)

# Convert distance to similarity
simmat = np.exp(-np.square(simmat))

# Set disconnected entries to zero
simmat[unconnected_indices] = 0
print("{} out of {} values set to zero".format(len(simmat[simmat == 0]), len(simmat)))

# Restore shape
simmat = simmat.reshape(dismat.shape)

# Fill diagonal with the maximum affinity
np.fill_diagonal(simmat, np.max(simmat))

G = palsgraph.make_graph(simmat, labels=labels)

#####################################################################################
# Find community

comp = girvan_newman(G)

#####################################################################################
# Show graph

max_shown = 2
shown_count = 1
for communities in islice(comp, max_shown):

    outfilename = 'graph-' + str(shown_count) + '.png'
    print("Possibility ", shown_count, " in " + outfilename)

    pos = palsgraph.getpos(G, communities) # Find nodes layout using pals

    colorize = True
    if colorize:
        color_map = palsgraph.gen_colormap(G, communities);
    else:
        color_map = ['grey']

    plt.figure(figsize=(17, 15))
    nx.draw(G, pos=pos, node_color=color_map, edge_color='grey', with_labels=True)
    plt.savefig(outfilename)

    shown_count += 1
