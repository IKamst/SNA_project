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

# Print information on degree centrality and plot the degree probabilities.
def print_plot_degree_distributions(ax, degrees, graph, label):
    degree_values = [degrees.get(vertex, 0) for vertex in graph.nodes()]
    mean_degree = statistics.mean(degree_values)
    print("Mean degree " + label + ": " + str(mean_degree))
    median_degree = statistics.median(degree_values)
    print("Median degree " + label + ": " + str(median_degree))
    min_degree = min(degree_values)
    print("Min degree " + label + ": " + str(min_degree))
    max_degree = max(degree_values)
    print("Max degree " + label + ": " + str(max_degree))
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
    print_plot_degree_distributions(ax, in_degrees, graph, "in-degree")
    # Out-degree
    out_degrees = dict(graph.out_degree())
    print_plot_degree_distributions(ax, out_degrees, graph, "out-degree")
    # All degrees
    total_degrees = dict(graph.degree())
    print_plot_degree_distributions(ax, total_degrees, graph, "total degree")

    # Make the degree distribution plot
    plt.legend(loc="upper left")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Degree distribution")
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

# Calculate relatively simple metrics and measures.
def calculate_metrics(graph):
    # Calculate the number of vertices
    n_vertices = graph.number_of_nodes()
    print("Number of vertices: " + str(n_vertices))
    # Calculate the number of edges
    n_edges = graph.number_of_edges()
    print("Number of edges: " + str(n_edges))
    # Calculate the degree distribution + degree centrality
    calculate_degree_distribution(graph)
    # Calculate the density
    density = nx.density(graph)
    print("Density: " + str(density))
    # Calculate the network diameter
    calculate_network_diameter(graph)





# Temporary. Using a simple graph right now.
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


