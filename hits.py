import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt


def plot_hits(hubs, authorities):
    plt.figure()
    plt.bar(list(hubs.keys())[:20], list(hubs.values())[:20])
    plt.title("Top 20 vertices with highest hub score for non-rumours", fontsize = 16)
    plt.xlabel("Vertex", fontsize = 16)
    plt.ylabel("Hub score", fontsize = 16)
    ax = plt.gca()
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=80)
    plt.yticks(fontsize = 14)
    plt.xticks(fontsize = 14)
    plt.savefig(r'hub_scores_non_r.png', bbox_inches = "tight")
    plt.tight_layout()
    plt.figure()
    plt.bar(list(authorities.keys())[:20], list(authorities.values())[:20])
    plt.title("Top 20 vertices with highest authority score for non-rumours", fontsize = 16)
    plt.xlabel("Vertex", fontsize = 16)
    plt.ylabel("Authority score", fontsize = 16)
    ax = plt.gca()
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=80)
    plt.yticks(fontsize = 14)
    plt.xticks(fontsize = 14)
    plt.savefig(r'authority_scores_non_r.png', bbox_inches = "tight")
    plt.show()

# Calculate the HITS and Pagerank scores for all vertices, show the first 20
def calculate_hits(graph):
    hits = nx.hits(graph)
    hubs = dict(sorted(hits[0].items(), key=lambda item: item[1], reverse = True))
    authorities = dict(sorted(hits[1].items(), key=lambda item: item[1], reverse = True))
    print("HITS 20 best scoring hubs: " + str(list(hubs.items())[:20]))
    print("HITS 20 best scoring authorities: " + str(list(authorities.items())[:20]))
    plot_hits(hubs, authorities)
    pagerank = dict(sorted(nx.pagerank(graph).items(), key=lambda item: item[1], reverse = True))
    print("Pagerank 20 best scoring: " + str(list(pagerank.items())[:20]))

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