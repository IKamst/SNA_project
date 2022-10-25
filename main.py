import networkx as nx
import matplotlib.pyplot as plt

#from preprocessing import read_data_file

testbool=True

def main():
    # Call to file and function to read data.

    if testbool==True:
        from test import read_data_file
        read_data_file()
    else:
        from preprocessing import read_data_file
        G = nx.complete_graph(6)
        nx.draw_networkx(G)
        plt.savefig("graph.png")
        plt.show()
        non_rumour_graph = nx.DiGraph()
        read_data_file(non_rumour_graph)


if __name__ == "__main__":
    main()
