from communities import make_final_plot
from main import create_load_structure


def create_community_structure(non_rumour_graph, rumour_graph, full_graph):
    nr_nodes = []
    r_nodes = []
    nr_r_nodes =[]
    for node in full_graph.nodes():
        if node in non_rumour_graph.nodes() and node in rumour_graph.nodes():
            nr_r_nodes.append(node)
        elif node in non_rumour_graph.nodes():
            nr_nodes.append(node)
        elif node in rumour_graph.nodes():
            r_nodes.append(node)
    print("Non-rumour nodes: " + str(len(nr_nodes)))
    print("Rumour nodes: " + str(len(r_nodes)))
    print("Both nodes: " + str(len(nr_r_nodes)))
    communities = [nr_nodes, r_nodes, nr_r_nodes]
    make_final_plot(full_graph, communities, "Full network, coloured by rumour and non-rumour")
    return


def read_in_graphs():
    non_rumour_graph = create_load_structure(False, True, True, False, False)
    rumour_graph = create_load_structure(False, True, False, True, False)
    full_graph = create_load_structure(False, True, False, False, True)
    if non_rumour_graph is None or rumour_graph is None or full_graph is None:
        create_load_structure(True, False, True, True, True)
        read_in_graphs()
    create_community_structure(non_rumour_graph, rumour_graph, full_graph)
    return


if __name__ == "__main__":
    read_in_graphs()