import networkx as nx
import matplotlib.pyplot as plt

from preprocessing import read_data_file


def main():
    # Call to file and function to read data.

    # G = nx.complete_graph(6)
    # nx.draw_networkx(G)
    # plt.savefig("graph.png")
    # plt.show()
    non_rumour_graph = nx.DiGraph()
    read_data_file(non_rumour_graph)

if __name__ == "__main__":
    main()
