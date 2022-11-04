import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt
import statistics

# number of vertices, number of edges, degree distribution
# (in-degree and out degree), centrality indices, clustering
# coefficient, network diameter, density, number of
# connected components and, size of the connected
# components.

def print_min_max_mean_median(metrics, label):
    mean_metrics = statistics.mean(metrics)
    print("Mean " + label + ": " + str(mean_metrics))
    median_metrics = statistics.median(metrics)
    print("Median " + label + ": " + str(median_metrics))
    min_metrics = min(metrics)
    print("Min " + label + ": " + str(min_metrics))
    max_metrics = max(metrics)
    print("Max " + label + ": " + str(max_metrics))

# Print information on degree centrality and plot the degree probabilities.
def print_plot_degree_distributions(ax, degrees, graph, label):
    degree_values = [degrees.get(vertex, 0) for vertex in graph.nodes()]
    print_min_max_mean_median(degree_values, "degree " + label)
    max_degree = max(degree_values)
    max_degree_node = {key for key, value in degrees.items() if value == max_degree}
    print("Max degree vertex " + label + ": " + str(max_degree_node))
    degree_prob= [ 0 for degree in range(max_degree + 1)]
    for value in degree_values:
        degree_prob[value] += 1
    n_vertices = graph.number_of_nodes()
    for index in range(len(degree_prob)):
        degree_prob[index] = degree_prob[index] / n_vertices

    ax.plot(range(len(degree_prob)), degree_prob, 'o-', label = label)

# Calculate the degree distribution and degree centrality.
# TODO make plot readable (increase font etc)
def calculate_degree_distribution(graph):
    # Initialise the plot
    fig, ax = plt.subplots()

    # In-degree
    in_degrees = dict(graph.in_degree())
    print_plot_degree_distributions(ax, in_degrees, graph, "In-degree")
    # Out-degree
    out_degrees = dict(graph.out_degree())
    print_plot_degree_distributions(ax, out_degrees, graph, "Out-degree")
    # All degrees
    total_degrees = dict(graph.degree())
    print_plot_degree_distributions(ax, total_degrees, graph, "Total degree")

    # Make the degree distribution plot
    plt.xlim([0, 20])
    plt.legend(loc="upper right", fontsize = 15)
    plt.xlabel("Degree", fontsize = 18)
    plt.ylabel("Probability", fontsize = 18)
    plt.title("Degree distribution rumours", fontsize = 18)
    plt.yticks(fontsize = 15)
    plt.xticks(fontsize = 15)
    plt.savefig("degree_distribution", bbox_inches = "tight")
    plt.show()

# Calculate the network diameter: the longest shortest path in the network
def calculate_network_diameter(graph):
    # First find all shortest paths
    path_lengths = dict(nx.all_pairs_shortest_path_length(graph))
    # Loop over the shortest paths and keep track of what starting and ending vertices have the maximum shortest path length
    max_length = -1
    max_starting_vertices = []
    max_ending_vertices = []
    for starting_vertex, combinations in path_lengths.items():
        for ending_vertex, length in combinations.items():
            if length > max_length:
                max_length = length
                max_starting_vertices = []
                max_ending_vertices = []
                max_starting_vertices.append(starting_vertex)
                max_ending_vertices.append(ending_vertex)
            elif length == max_length:
                max_starting_vertices.append(starting_vertex)
                max_ending_vertices.append(ending_vertex)
    print("Network diameter: " + str(max_length))
    print("Starting vertices for this diameter: " + str(max_starting_vertices))
    print("Corresponding ending vertices for this diameter: " + str(max_ending_vertices))

# Determine the connected components and their sizes
def calculate_connected_components(graph):
    n_strongly_connected = nx.number_strongly_connected_components(graph)
    print("Number of strongly connected components: " + str(n_strongly_connected))
    strongly_connected = [(component, len(component)) for component in sorted(nx.strongly_connected_components(graph), key = len, reverse = True)]
    print(nx.strongly_connected_components)
    print(max(nx.strongly_connected_components(graph), key=len))
    print("20 largest strongly connected components (with length): "+ str(strongly_connected[:20]))
    mean_strongly_connected = sum(length for _, length in strongly_connected) / n_strongly_connected
    print("Mean length strongly connected components: "+ str(mean_strongly_connected))
    max_strongly_connected =max(length for _, length in strongly_connected)
    print("Max length strongly connected components: " + str(max_strongly_connected))
    n_weakly_connected = nx.number_weakly_connected_components(graph)
    print("Number of weakly connected components: " + str(n_weakly_connected))
    weakly_connected = [(component, len(component)) for component in sorted(nx.weakly_connected_components(graph), key = len, reverse = True)]
    # TODO fix this: doesn't seem sorted (or top 20)?
    print("20 largest weakly connected components (with length): " + str(weakly_connected[:20]))
    mean_weakly_connected = sum(length for _, length in weakly_connected) / n_weakly_connected
    print("Mean length weakly connected components: "+ str(mean_weakly_connected))
    max_weakly_connected = max(length for _, length in weakly_connected)
    print("Max length weakly connected components: " + str(max_weakly_connected))

# Calculate centralities other than the degree centrality
def calculate_centralities(graph):
    # Calculate the eigenvector centrality
    eigenvector_centrality = list(nx.eigenvector_centrality(graph, max_iter=600).values())
    print(eigenvector_centrality)
    print_min_max_mean_median(eigenvector_centrality, "eigenvector centrality")
    # Calculate the closeness centrality
    # TODO find out what kind of definition of closeness centrality is used (for report)
    closeness_centrality = list(nx.closeness_centrality(graph, wf_improved=False).values())
    print_min_max_mean_median(closeness_centrality, "closeness centrality")
    # Calculate the betweenness centrality
    # TODO find out what sample of nodes to use (if you do not include k it takes a realllly long time)
    n_nodes = graph.number_of_nodes()
    betweenness_centrality = list(nx.betweenness_centrality(graph).values())
    print_min_max_mean_median(betweenness_centrality, "betweenness centrality")

# Calculate metrics and measures.
def calculate_metrics(graph):
    # Calculate the number of vertices
    n_vertices = graph.number_of_nodes()
    print("Number of vertices: " + str(n_vertices))
    # Calculate the number of edges
    n_edges = graph.number_of_edges()
    print("Number of edges: " + str(n_edges))
    # Calculate the degree distribution + degree centrality
    calculate_degree_distribution(graph)
    # Calculate other centralities
    calculate_centralities(graph)
    # Calculate the clustering coefficient
    clustering = nx.clustering(graph)
    print_min_max_mean_median((clustering.values()), "clustering coefficient")
    # Calculate the network diameter
    calculate_network_diameter(graph)
    # Calculate the density
    density = nx.density(graph)
    print("Density: " + str(density))
    # Determine the connected components and their size
    calculate_connected_components(graph)


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
    calculate_metrics(simple_graph)


