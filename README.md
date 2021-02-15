# PalsGraph: a module for use with NetworkX to display communities in graph
PalsGraph provides three methods to enable easy use of NetworkX to display the communities discovered in a graph.

* make\_graph: Create a NetworkX graph with labels
* getpos: Calculate the optimal positions for visualizing the graph nodes based on the communities
* gen_colormap: Generate a colormap where each community is given a unique color

![logo](./logo.png)

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

Assume that we have a distance matrix in `distmat`, with the labels of the entities in `labels`. 
The following constructs a NetworkX graph from the distance matrix. A label-less graph is generated if `labels=None`, and disconnected vertices will not be shown if `show_singletons=False`.

```Python
import palsgraph
G = palsgraph.make_graph(distmat, labels=labels, show_singletons=False)
```
Then, suppose we use a method in NetworkX to discover the communities in `G`. (In the following, Garvin-Newman is used.)
```Python
import networkx as nx
comp = nx.algorithms.community.centrality.girvan_newman(G)
```
NetworkX will return several possible ways to organize the graph into communities. Each possibility is an array of arrays. For example, `({'A'}, {'B', 'C'}, {'D', 'E'})`. In which case, `'A'` forms a community, `'B'`, `'C'` form another, and `'D'`, `'E'` likewise form another community.

The following codes show how each possibility can be enumerated (using islice) and visualized using palsgraph.
```Python
import matplotlib.pyplot as plt
from itertools import islice
max_shown = 3
shown_count = 1
for communities in islice(comp, max_shown): # For each possible set of communities

    # Find optimal positions for displaying the communities in the graph
    pos = palsgraph.getpos(G, communities)

    # Generate a colormap
    color_map = palsgraph.gen_colormap(G, communities)

    # Draw graph and save to output file
    plt.figure(figsize=(17, 15))
    nx.draw(G, pos=pos, node_color=color_map, edge_color='grey', with_labels=True)
    outfilename = 'graph-' + str(shown_count) + '.png'
    plt.savefig(outfilename)

    shown_count += 1
```

If you implement your own community detection algorithm, just output the communities in the form of `({'A'}, {'B', 'C'}, {'D', 'E'})` and you will be able to use PalsGraph just like in the example above.

### Sample output
The following gives an example of the graphs generated using PalsGraph. Note that the graph connectedness is as given in the distance matrix, but the colors and positions are based only on the communities discovered. In this example, the communities discovered are mainly in accordance with the connectedness of graph structure, except for a few vertices.

![Sample Output Graph](./tests/graph-1.png)

## Help
If you have any questions or require assistance using PalsGraph, please contact us with kalngyk@gmail.com.

## Credits
PalsGraph is written by Yujin Yao and Yen Kaow Ng under the supervision of Honwai Leong.
