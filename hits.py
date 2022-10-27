import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt

# Calculate the HITS and Pagerank scores for all vertices
def calculate_hits(graph):
    hits = nx.hits(graph)
    hubs = dict(sorted(hits[0].items(), key=lambda item: item[1], reverse = True))
    authorities = dict(sorted(hits[1].items(), key=lambda item: item[1], reverse = True))
    print("HITS hubs: " + str(hubs))
    print("HITS authorities: " + str(authorities))
    pagerank = dict(sorted(nx.pagerank(graph).items(), key=lambda item: item[1], reverse = True))
    print("Pagerank: " + str(pagerank))

# Temporary. Using a simple graph right now.
# TODO: use actual graph
if __name__ == "__main__":
    simple_graph = nx.DiGraph()
    weighted_edge_list = [(u, v, random.random()) for u, v in itertools.permutations(range(4), 2)]
    simple_graph.add_weighted_edges_from(weighted_edge_list)
    simple_graph.remove_edge(1, 2)
    simple_graph.remove_edge(0, 1)
    simple_graph.remove_edge(0, 2)
    simple_graph.remove_edge(0, 3)
    nx.draw_networkx(simple_graph)
    plt.show()
    calculate_hits(simple_graph)