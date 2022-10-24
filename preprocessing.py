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
                        # Closing file
                        f.close()
    graph.add_weighted_edges_from([(553187282295877632, 553187515671138305, 1)])
    print(graph)
    pos = nx.random_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    plt.savefig("graph.png")
    plt.show()

#check if weight exists, if so add 1 to the weight (weight increases with interaction between two users)


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
