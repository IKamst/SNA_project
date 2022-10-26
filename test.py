import json
import pandas as pd
import os
import re

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pylab as pl



# testing how to make a graph from a dictionary with only one thing
def read_data_file():
    bigdictionary = {}
    wd = os.getcwd()
    path = wd + '/charliehebdo-all-rnr-threads/non-rumours/552784600502915072'

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        # if os.path.isfile(file_path):
        if file == "structure.json":
            f = open(file_path)
            # Load the data as a dictionary.
            data = json.load(f)
            fakedata = {'a':{'c':{}}, 'b':{'c':{'d':{}}, 'a':{}}}
            #key = '552784600502915072'
            newdata = dictionary_unfold(data, {})
            #newdata = nx.from_dict_of_dicts(fakedata,create_using=nx.DiGraph, multigraph_input=False)
            print(newdata)
            G = nx.DiGraph(newdata)
            nx.draw_networkx(G, with_labels=False, node_size=50)
            plt.savefig("bigdictionarygraph.png")
            plt.show()
    return


# given a recursive dictionary of dictionaries,
def dictionary_unfold(data, big_dictionary):
    #base case
    if isinstance(data,list):
        return big_dictionary
    else:
        #loop over all the keys in data
        for key, value in data.items():
            # check if the key already exists
            if big_dictionary.get(key) is None:
                # only keep "first level entries" of the dict in the value
                if not isinstance(data[key], list): #when data[key] = []
                    big_dictionary[key] = list(data[key].keys())
                else:
                     big_dictionary[key] = data[key]
            else:
                # if the key already exists, add to value
                big_dictionary[key] = big_dictionary[key] + list(data[key].keys()) # append the existing list
                big_dictionary[key] = [*set((big_dictionary[key]))]  # remove doubles
            big_dictionary = dictionary_unfold(data[key], big_dictionary)
        return big_dictionary




def determine_nodes_and_edges(graph, main_node, values):
    # Prints the source tweet.
    # print(main_node)
    graph.add_node(main_node)
    # Prints the tweets linked to the source tweet and their inner structure.
    # TODO how to get the structure if tweets continue further?
    # print(values)
    out = re.split(r"[:|,]", str(values))
    # print(out)
    # for elem in out:
    #     print(elem)
    return graph
