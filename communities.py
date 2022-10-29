import copy
import itertools
import random

import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from networkx import find_cliques
from networkx.algorithms.community import modularity, girvan_newman
import seaborn as sns

def make_final_plot(graph, communities):
    color_map = []
    get_colours = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colours = get_colours(len(communities))
    for node in graph.nodes():
        for i in range(len(communities)):
            if node in communities[i]:
                color_map.append(colours[i])
    plt.figure()
    nx.draw(graph, node_color=color_map, with_labels=True)
    plt.show()
    return


def girvan_newman_all(graph):
    temp_graph = copy.deepcopy(graph)
    best = copy.deepcopy(graph)
    best_clusters = False
    max_mod = 0
    gn_model = girvan_newman(temp_graph)
    # TODO determine how many runs
    limited_runs = itertools.takewhile(lambda c: len(c) <= graph.number_of_nodes(), gn_model)
    for communities in limited_runs:
        print(tuple(sorted(c) for c in communities))
        mod = modularity(graph, communities)
        print("Modularity:" + str(mod))
        if mod > max_mod:
            max_mod = mod
            best = copy.deepcopy(communities)
    return best, max_mod


def cliques(graph):
    # TODO ideas on how to plot this?
    max_cliques = list(find_cliques(graph))
    print("Maximal cliques: " + str(max_cliques))
    nodes = []
    cnt_cliques = []
    for node in graph.nodes():
        cnt = 0
        for clique in max_cliques:
            if node in clique:
                cnt = cnt + 1
        cnt_cliques.append(cnt)
        nodes.append(str(nodes))
    df = pd.DataFrame({"Node": nodes,
                       "Number of cliques": cnt_cliques})
    df.sort_values("Number of cliques")
    plt.figure()
    sns.barplot(x='Node', y="Number of cliques", data=df)
    plt.show()
    return


def main():
    graph = nx.random_k_out_graph(20, 3, 0.5)
    nx.draw_networkx(graph)
    plt.show()
    # Create an undirected version of this graph.
    # reciprocal: bool (optional) (if True only keep edges that appear in both directions).
    undirected_graph = graph.to_undirected()
    nx.draw_networkx(undirected_graph)
    plt.show()
    # Find the maximal cliques
    cliques(undirected_graph)
    # Find the best partitioning using Girvan Newman with modularity
    best, max_mod = girvan_newman_all(undirected_graph)
    print("Maximum modularity: " + str(max_mod))
    print("For best communities partitioning: " + str(best))
    make_final_plot(undirected_graph, best)


if __name__ == "__main__":
    main()
