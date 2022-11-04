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

from create_homophily_dictionary import read_data_homophily


# Make a plot of the graph. Giving each community different colour in nodes.
def make_final_plot(graph, communities, text, positioning):
    color_map = []
    # Create random colours for each of the communities.
    get_colours = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colours = get_colours(len(communities))
    # Loop over all nodes and add the correct colour based on community to the colormap.
    for node in graph.nodes():
        for i in range(len(communities)):
            if node in communities[i]:
                color_map.append(colours[i])
    # Make the graph using the colours from the communities.
    plt.figure()
    nx.draw_networkx(graph, node_color=color_map, node_size=10, with_labels=False, width=0.5, pos=positioning)
    plt.title(text, fontsize=15)
    plt.savefig(text + ".png")
    plt.show()
    return


# A full run of the Girvan-Newman partitioning algorithm.
def girvan_newman_all(graph):
    temp_graph = copy.deepcopy(graph)
    best = []
    max_mod = 0
    gn_model = girvan_newman(temp_graph)
    k = 50
    # Apply Girvan-Newman for 50 iterations.
    for communities in itertools.islice(gn_model, k):
        # print(tuple(sorted(c) for c in communities))
        # print(len(communities))
        # Calculate the modularity of the current communities.
        mod = modularity(graph, communities)
        print("Modularity:" + str(mod))
        # Save the current modularity and community if better than all previous modularities.
        if mod > max_mod:
            max_mod = mod
            best = copy.deepcopy(communities)
    # Print the maximum modularity and best partitioning.
    print("Maximum modularity: " + str(max_mod))
    print("For best communities partitioning: " + str(best))
    print("Number components:", str(len(best)))
    return best, max_mod


# Determine the maximal cliques and output relevant information.
def determine_cliques(graph):
    # Find the maximal cliques.
    max_cliques = list(find_cliques(graph))
    print("Maximal cliques: " + str(max_cliques))
    # Determine the size of each clique.
    len_cliques = []
    for clique in max_cliques:
        len_cliques.append(len(clique))
    # Output maximum, minimum, mean size of clique.
    print("Maximum size of cliques: " + str(max(len_cliques)))
    print("Minimum size of cliques: " + str(min(len_cliques)))
    print("Mean size of cliques: " + str(np.mean(len_cliques)))
    # For each node determine how many cliques it is part of.
    nodes = []
    cnt_cliques = []
    for node in graph.nodes():
        cnt = 0
        for clique in max_cliques:
            if node in clique:
                cnt = cnt + 1
        cnt_cliques.append(cnt)
        nodes.append(str(node))
    # Make a dataframe saving the node and its number of cliques.
    df = pd.DataFrame({"Node": nodes,
                       "Number of cliques": cnt_cliques})
    df.sort_values(by=["Number of cliques"], inplace=True, ascending=False)
    # Make a plot of the 20 vertices part of the most cliques.
    plt.figure()
    plt.bar(df["Node"][0:20], df["Number of cliques"][0:20])
    plt.title("Top 20 vertices with most cliques for graph", fontsize=15)
    plt.xlabel("Vertex", fontsize=14)
    plt.ylabel("Number of cliques", fontsize=14)
    ax = plt.gca()
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=80)
    plt.tight_layout()
    plt.savefig(r'cliques_nonrumour.png')
    plt.show()
    return


# Determine bridges in the graph.
def determine_bridges(graph, positioning):
    # Find the bridges.
    bridges_list = list(bridges(graph))
    # Output information about the bridges.
    print("Bridges: " + str(bridges_list))
    print("Length of bridges: " + str(len(bridges_list)))
    print("Connected components: " + str(nx.number_connected_components(graph)))
    # If there are bridges, use the bridge components to make a plot based on those.
    if len(bridges_list) > 0:
        communities = sorted(map(sorted, bridge_components(graph)))
        print("Number of bridge components: " + str(len(communities)))
        print(communities)
        make_final_plot(graph, communities, "Rumour graph coloured by bridge components", positioning)
    return bridges_list


# Do a homophily analysis on account id versus being verified.
def homophily(graph, id_verified_dic):
    verified = []
    not_verified = []
    # Add the nodes to the verified or not verified array.
    for key in id_verified_dic:
        if id_verified_dic[key]: # If verified
            verified.append(str(key))
        else:
            not_verified.append(str(key))
    # The communities correspond to the verified and not verified users.
    communities = (verified, not_verified)
    print(communities)
    # Determine the fraction of verified and not verified users.
    total = len(verified) + len(not_verified)
    fraction_verified = len(verified)/total
    fraction_not_verified = len(not_verified)/total
    print("Fraction verified users: " + str(fraction_verified))
    print("Fraction unverified users: " + str(fraction_not_verified))
    # Determine the predicted fraction of verified = not verified edges.
    predicted_frac_verified_not_verified_edges = 2 * fraction_verified * fraction_not_verified
    # Count the edges of each type.
    cnt_verified_not_verified_edges = 0
    cnt_verified_verified = 0
    cnt_not_not = 0
    for edge in graph.edges():
        if edge[0] in verified and edge[1] in not_verified:
            cnt_verified_not_verified_edges = cnt_verified_not_verified_edges + 1
        if edge[0] in not_verified and edge[1] in verified:
            cnt_verified_not_verified_edges = cnt_verified_not_verified_edges + 1
        if edge[0] in verified and edge[1] in verified:
            cnt_verified_verified = cnt_verified_verified + 1
        if edge[0] in not_verified and edge[1] in not_verified:
            cnt_not_not = cnt_not_not + 1
    # Determine the actual fraction of verified - not verified edges.
    actual_frac_verified_not_verified_edges = cnt_verified_not_verified_edges / graph.number_of_edges()
    # Print the fraction of each edge type.
    print("Predicted fraction verified - not verified edges: " + str(predicted_frac_verified_not_verified_edges))
    print("Actual fraction verified - not verified edges: " + str(actual_frac_verified_not_verified_edges))
    print("Verified - verified edges: " + str(cnt_verified_verified/graph.number_of_edges()))
    print("Not verified - not verified edges: " + str(cnt_not_not/graph.number_of_edges()))
    return communities


# Function that runs all code related to community analysis.
def community_analysis(graph, positioning, non_rumour_bool):
    # Create an undirected version of this graph.
    undirected_graph = graph.to_undirected()
    print("Undirected graph:")
    plt.figure()
    nx.draw_networkx(undirected_graph, node_size=10, with_labels=False, width=0.5, pos=positioning)
    plt.title("Undirected version of the network")
    plt.show()
    # Find the maximal cliques.
    determine_cliques(undirected_graph)
    # Find the best partitioning using Girvan Newman with modularity.
    best, max_mod = girvan_newman_all(undirected_graph)
    # Find the bridges of the network.
    bridges_list = determine_bridges(undirected_graph, positioning)
    make_final_plot(undirected_graph, best, "Rumour graph coloured by Girvan Newman communities", positioning)
    # Save a dictionary of id's to whether the account is verified.
    id_to_verified_dic = {}
    if non_rumour_bool:
        id_to_verified_dic = read_data_homophily('non-rumours', id_to_verified_dic)
    else:
        id_to_verified_dic = read_data_homophily('rumours', id_to_verified_dic)
    # Do homophily analysis and plot the communities.
    communities = homophily(undirected_graph, id_to_verified_dic)
    make_final_plot(undirected_graph, communities, "Rumour graph coloured based on verified or not", positioning)


# Small directed graph to try out the functions.
if __name__ == "__main__":
    directed_graph = nx.random_k_out_graph(20, 3, 0.5)
    positioning = nx.spring_layout(directed_graph)
    nx.draw(directed_graph)
    plt.show()
    community_analysis(directed_graph, positioning, True)
