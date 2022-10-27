import networkx as nx
import matplotlib.pyplot as plt
from preprocessing import read_data_file, create_digraph, dict_append
from json import load, dump
from os import getcwd

testbool=True

def main():
    # Call to file and function to read data.
        # nonrumour_dict = read_data_file('non-rumours')
        # rumour_dict = read_data_file('rumours')
    wd = getcwd()

    nrf = open(wd + '\structure-non-rumours.json')
    nrdata = load(nrf)
    nonrumourgraph = create_digraph(nrdata)
    print(nonrumourgraph)

    rf = open(wd + '\structure-rumours.json')
    rdata = load(rf)
    rumourgraph = create_digraph(rdata)
    print(rumourgraph)

        # full_dict = dict_append(nrdata, rdata)
        # fullgraph = create_digraph(full_dict)
        # out_file = open("structure-full-dictionary" + ".json", "w")
        # dump(full_dict, out_file, indent="")
        # print(fullgraph)



if __name__ == "__main__":
    main()
