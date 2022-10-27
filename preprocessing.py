import json
import os
import re

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

# Reads the data from the structure.json file.
# TODO how to save the data to get the full correct structure?
# TODO input to save files for rumour and non-rumour?
def read_data_file(graph):
    # Get the current working directory and ensure we are on the correct path.
    bigdictionary = {}
    wd = os.getcwd()
    print("Current working directory: {0}".format(wd))
    path = wd + '/charliehebdo-all-rnr-threads/non-rumours'
    print(path)
    # Loop over the directories for that path.
    for directory_name in os.listdir(path):
        directory = os.path.join(path, directory_name)
        if os.path.isdir(directory):
            print("DIRECTORY" + directory)
            # Loop over the files in that directory.
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    # Open the file if it contains the structure of the tweets.
                    if file == "structure.json":
                        f = open(file_path)
                        # Load the data as a dictionary.
                        data = json.load(f)
                        print(data)
                        for key in data:
                            graph = determine_nodes_and_edges(graph, key, data[key])
                            bigdictionary[key] = data
                            while not data:
                                data = bigdictionary[key]
                                bigdictionary[data] = data
                        # Closing file
                        f.close()
    graph.add_weighted_edges_from([(553187282295877632, 553187515671138305, 1)])
    print(graph)
    pos = nx.random_layout(graph)
    nx.draw_networkx(graph, pos, node_size=10, arrowsize=5, with_labels=False)
    #plt.savefig("graph.png")
    plt.show()

    graph2 = nx.DiGraph(bigdictionary)
    print(bigdictionary)
    print(graph2)
    nx.draw_networkx(graph2, pos, node_size=5, arrowsize=1, with_labels=False)

    plt.show()


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
    print(main_node)
    graph.add_node(main_node)
    # Prints the tweets linked to the source tweet and their inner structure.
    # TODO how to get the structure if tweets continue further?
    print(values)
    out = re.split(r"[:|,]", str(values))
    print(out)
    for elem in out:
        print(elem)
    return graph
