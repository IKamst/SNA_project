from matplotlib import pyplot as plt
from networkx import planar_layout

from communities import community_analysis
from preprocessing import read_data_file, create_digraph, dict_append
from metrics import calculate_metrics
from hits import calculate_hits
from json import load, dump
from os import getcwd
import networkx as nx
import pygraphviz

from communities import community_analysis
from hits import calculate_hits
from longitudinal import longitudinal_analysis
from metrics import calculate_metrics
from preprocessing import read_data_file, create_digraph, dict_append


def create_load_structure(CREATE_STRUCTURE_FILES, OPEN_STRUCTURE_FILES, NON_RUMOUR, RUMOUR, FULL):
    # Call to file and function to read data.
    wd = getcwd()
    if CREATE_STRUCTURE_FILES:
        if NON_RUMOUR:
            read_data_file('non-rumours')
        if RUMOUR:
            read_data_file('rumours')
        if FULL:
            rdata = read_data_file('rumours')
            nrdata = read_data_file('non-rumours')
            if rdata is not None and nrdata is not None:
                full_dict = dict_append(nrdata, rdata)
                out_file = open(wd + "/structures/structure-full-dictionary" + ".json", "w")
                dump(full_dict, out_file, indent="")
            else:
                print("An error has occured.")
                print(nrdata)
                print(rdata)
        return None

    if OPEN_STRUCTURE_FILES:
        if NON_RUMOUR:
            nrf = open(wd + '\structures\structure-non-rumours.json')
            nrdata = load(nrf)
            return create_digraph(nrdata)


        if RUMOUR:
            rf = open(wd + '\structures\structure-rumours.json')
            rdata = load(rf)
            return create_digraph(rdata)

        if FULL:
            f = open(wd + '\structures\structure-full-dictionary.json')
            fdata = load(f)
            return create_digraph(fdata)
    return
def main():
    g = create_load_structure(False, True, True, True, True)
    if g is None:
        print("The structure files have been created. Please set OPEN_STRUCTURE_FILES to True.")
    else:
        print(g)
        undirected_graph = g.to_undirected()
        positioning = nx.spring_layout(undirected_graph)
        nx.draw_networkx(g, node_size=10, with_labels=False, width=0.5, pos=positioning)
        plt.title("Directed version of the network")
        plt.show()
        calculate_metrics(g)
        calculate_hits(g)
        community_analysis(g, positioning)
        longitudinal_analysis()


if __name__ == "__main__":
    main()
