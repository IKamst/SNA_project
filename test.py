import json
import os
import re

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

#testing how to make a graph from a dictionary with only one thing
def read_data_file():

    bigdictionary = {}
    wd = os.getcwd()
    path = wd + '/charliehebdo-all-rnr-threads/non-rumours/552784600502915072'

    for file in os.listdir(path):
        file_path =os.path.join(path, file)
        # if os.path.isfile(file_path):
        if file == "structure.json":
            f = open(file_path)
            # Load the data as a dictionary.
            data = json.load(f)
            key = 552784600502915072
            value = data[key]
            for v in value:
                while v is not []:
                    value
            # graph = nx.DiGraph(data)
            # print(data)
            # pos = nx.random_layout(graph)
            # nx.draw_networkx(graph, pos)
            # plt.show()
            # for key in data:
            #     print(key)
            #     graph = determine_nodes_and_edges(graph, key, data[key])
            #     bigdictionary[key] = data[key]
            #     print(bigdictionary)
            #     # while not data:
            #     #     data = bigdictionary[key]
            #     #     bigdictionary[data] = data
            # # Closing file
            # f.close()

    return

#given a recursive dictionary of dictionaries,
def dictionary_unfold(data, big_dictionary):
    x = 1
    return x

#check if weight exists, if so add 1 to the weight (weight increases with interaction between two users)


def determine_nodes_and_edges(graph, main_node, values):
    # Prints the source tweet.
    #print(main_node)
    graph.add_node(main_node)
    # Prints the tweets linked to the source tweet and their inner structure.
    # TODO how to get the structure if tweets continue further?
    #print(values)
    out = re.split(r"[:|,]", str(values))
    #print(out)
    # for elem in out:
    #     print(elem)
    return graph
