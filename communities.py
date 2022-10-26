import copy
import networkx as nx
from matplotlib import pyplot as plt
from networkx import connected_components
from networkx.algorithms.community import louvain_partitions, modularity


# TODO calculate betweenness score if we do it ourselves.
def calculate_betweenness(output):
    return output


# # TODO Calculate the modularity Q.
# # TODO Repeat from step 2 if: if Q > 0.3 –max Modularity is the best partitioning into clusters
# def determine_if_best_clusters_own(original_graph, graph):
#     m = original_graph.number_of_edges()
#     print(m)
#     sum_A_min_p = 0
#     for node_i in graph.nodes():
#         for node_j in graph.nodes():
#             A_ij = 0
#             k_i = original_graph.degree(node_i)
#             k_j = original_graph.degree(node_j)
#             p_ij = k_i * k_j / (2 * m)
#             if graph.has_edge(node_i, node_j):
#                 A_ij = 1
#             sum_A_min_p = sum_A_min_p + A_ij - p_ij
#     modularity = sum_A_min_p / (2 * m)
#     print("Modularity own: " + str(modularity))
#     return False


def determine_if_best_clusters(original_graph, updated_graph):
    connected = connected_components(updated_graph)
    max_modularity = modularity(original_graph, connected)
    print("Modularity:" + str(max_modularity))
    return False, max_modularity


def girvan_newman_step(graph):
    betweenness_dict = nx.edge_betweenness_centrality(graph)
    # TODO calculate betweenness score ourselves?
    # output = 1
    # # Loop over all edges.
    # for edge in graph.edges():
    #     print(edge)
    #     # For each edge calculate the betweenness score
    #     betweenness = calculate_betweenness(output)
    #     betweenness_dict[edge] = betweenness
    #     output = output + 1
    # Sort the dictionary to get the edge with the highest betweenness score.
    # TODO remove random best if multiple best.
    sorted_scores = sorted(betweenness_dict.items(), key=lambda x: x[1], reverse=True)
    print(sorted_scores)
    best_edge = sorted_scores[0][0]
    # Remove the edge with the highest betweenness score
    graph.remove_edge(best_edge[0], best_edge[1])
    print(graph)
    return graph


def girvan_newman(graph):
    temp_graph = copy.deepcopy(graph)
    best = copy.deepcopy(graph)
    best_clusters = False
    max_mod = 0
    while temp_graph.number_of_edges() > 0 and not best_clusters:
        temp_graph = girvan_newman_step(temp_graph)
        if temp_graph.number_of_edges() > 0:
            best_clusters, mod = determine_if_best_clusters(graph, temp_graph)
            if mod > max_mod:
                max_mod = mod
                best = copy.deepcopy(temp_graph)
    print("max: " + str(max_mod))
    nx.draw_networkx(best)
    plt.show()
    return


def main():
    graph = nx.karate_club_graph()
    nx.draw_networkx(graph)
    plt.savefig("graph.png")
    plt.show()
    girvan_newman(graph)


if __name__ == "__main__":
    main()