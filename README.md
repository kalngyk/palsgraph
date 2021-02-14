# PalsGraph: a module for use with NetworkX to display communities in graph
PalsGraph provides three methods to enable easy use of NetworkX to display the communities discovered in a graph.

* make\_graph
* getpos
* gen_colormap


## Pre-requirements
* python3
* numpy>=1.16.1
* networkx
* seaborn
* pybind11~=2.6.1

## Installation

### Installation with pip
To install with pip, run the following from a terminal:
```Bash
pip install palsgraph
```

### Installation from Github
To clone the repository and install manually, run the following from a terminal:
```Bash
git clone https://github.com/kalngyk/palsgraph.git
cd palsgraph
python setup.py install
```

## Usage

### Quick start
The following codes demonstrates how to use the three functions provided by PalsGraph.

First, prepare a distance matrix, such as the following:
```Python
import numpy as np
from scipy.spatial.distance import squareform
simfilename = 'test.tsv'
X = np.genfromtxt(simfilename, delimiter='\t', encoding='utf8', dtype=None)
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
threshold = 0.75
dismat2 = dismat.copy()
np.fill_diagonal(dismat2, np.min(dismat))
dismat2 = dismat2.reshape((-1,))
dismat2[dismat2 > threshold] = 0
dismat2 = dismat2.reshape(dismat.shape)
```
The following constructs a NetworkX graph from the distance matrix
```Python
import palsgraph
G = palsgraph.make_graph(dismat2, labels=labels, show_singletons=False)
```
Find community using any method in NetworkX
```Python
import networkx as nx
comp = nx.algorithms.community.centrality.girvan_newman(G)
```
Show the communities discovered, as follows:
```Python
import matplotlib.pyplot as plt
from itertools import islice
max_shown = 2
shown_count = 1
for communities in islice(comp, max_shown):

    outfilename = 'graph-' + str(shown_count) + '.png'
    print("Possibility ", shown_count, " in " + outfilename)

    pos = palsgraph.getpos(G, communities) # Find nodes layout using pals

    colorize = True
    if colorize:
        color_map = palsgraph.gen_colormap(G, communities);  # Generate a colormap using pals
    else:
        color_map = ['grey']

    plt.figure(figsize=(17, 15))
    nx.draw(G, pos=pos, node_color=color_map, edge_color='grey', with_labels=True)
    plt.savefig(outfilename)

    shown_count += 1
```
### Sample output

![Sample Output Graph](./tests/graph-1.png)

## Help
If you have any questions or require assistance using PalsGraph, please contact us with kalngyk@gmail.com.
