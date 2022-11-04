import copy
import itertools
import random

import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from networkx import find_cliques, bridges
from networkx.algorithms.community import modularity, girvan_newman
from networkx.algorithms.connectivity import bridge_components


# Make a plot of the graph. Giving each community different colour in nodes.
def make_final_plot(graph, communities, text, positioning):
    color_map = []
    get_colours = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colours = get_colours(len(communities))
    for node in graph.nodes():
        for i in range(len(communities)):
            if node in communities[i]:
                color_map.append(colours[i])
    plt.figure()
    nx.draw_networkx(graph, node_color=color_map, node_size=10, with_labels=False, width=0.5, pos=positioning)
    plt.title(text, fontsize=15)
    plt.savefig(text + ".png")
    plt.show()
    return


def girvan_newman_all(graph):
    temp_graph = copy.deepcopy(graph)
    best = []
    max_mod = 0
    gn_model = girvan_newman(temp_graph)
    k = 50
    for communities in itertools.islice(gn_model, k):
        # print(tuple(sorted(c) for c in communities))
        # print(len(communities))
        mod = modularity(graph, communities)
        print("Modularity:" + str(mod))
        if mod > max_mod:
            max_mod = mod
            best = copy.deepcopy(communities)
    return best, max_mod


def determine_cliques(graph):
    max_cliques = list(find_cliques(graph))
    print("Maximal cliques: " + str(max_cliques))
    len_cliques = []
    for clique in max_cliques:
        len_cliques.append(len(clique))
    print("Maximum size of cliques: " + str(max(len_cliques)))
    print("Minimum size of cliques: " + str(min(len_cliques)))
    print("Mean size of cliques: " + str(np.mean(len_cliques)))
    nodes = []
    cnt_cliques = []
    for node in graph.nodes():
        cnt = 0
        for clique in max_cliques:
            if node in clique:
                cnt = cnt + 1
        cnt_cliques.append(cnt)
        nodes.append(str(node))
    df = pd.DataFrame({"Node": nodes,
                       "Number of cliques": cnt_cliques})
    df.sort_values(by=["Number of cliques"], inplace=True, ascending=False)
    plt.figure()
    plt.bar(df["Node"][0:20], df["Number of cliques"][0:20])
    plt.title("Top 20 vertices with most cliques for non-rumour graph", fontsize=15)
    plt.xlabel("Vertex", fontsize=14)
    plt.ylabel("Number of cliques", fontsize=14)
    ax = plt.gca()
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=80)
    plt.tight_layout()
    plt.savefig(r'cliques_nonrumour.png')
    plt.show()
    return


def determine_bridges(graph, positioning):
    bridges_list = list(bridges(graph))
    print("Bridges: " + str(bridges_list))
    print("Length of bridges: " + str(len(bridges_list)))
    print("Connected components: " + str(nx.number_connected_components(graph)))
    if len(bridges_list) > 0:
        communities = sorted(map(sorted, bridge_components(graph)))
        print("Number of bridge components: " + str(len(communities)))
        print(communities)
        make_final_plot(graph, communities, "Rumour graph coloured by bridge components", positioning)
    return bridges_list


def community_analysis(graph, positioning):
    # Create an undirected version of this graph.
    # reciprocal: bool (optional) (if True only keep edges that appear in both directions).
    undirected_graph = graph.to_undirected()
    print("Undirected graph:")
    plt.figure()
    nx.draw_networkx(undirected_graph, node_size=10, with_labels=False, width=0.5, pos=positioning)
    plt.title("Undirected version of the network")
    plt.show()
    # Find the maximal cliques
    determine_cliques(undirected_graph)
    # Find the best partitioning using Girvan Newman with modularity
    best, max_mod = girvan_newman_all(undirected_graph)
    print("Maximum modularity: " + str(max_mod))
    print("For best communities partitioning: " + str(best))
    print("Number components:", str(len(best)))
    make_final_plot(undirected_graph, best, "Rumour graph coloured by Girvan Newman communities", positioning)
    bridges_list = determine_bridges(undirected_graph, positioning)
    # TODO homophily analysis. Need to think of which factors to consider
    # Homophily is the principle that we tend to be similar to our
    # friends. -> Intrinsic and contextual


if __name__ == "__main__":
    directed_graph = nx.random_k_out_graph(20, 3, 0.5)
    positioning = nx.spring_layout(directed_graph)
    nx.draw(directed_graph)
    plt.show()
    community_analysis(directed_graph, positioning)
