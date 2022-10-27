import json
import pandas as pd
import os
import re

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pylab as pl



# testing how to make a graph from a dictionary with only one thing
def read_data_file(rumourboolpath):
    bigdictionary = {}
    wd = os.getcwd()
    path = wd + '\charliehebdo-all-rnr-threads/' + rumourboolpath
    for directory_name in os.listdir(path):
        direc_path = os.path.join(path, directory_name)
        if os.path.isdir(direc_path):
            # Loop over the files in that directory.
            for file in os.listdir(direc_path):
                file_path = os.path.join(direc_path, file)
                # if os.path.isfile(file_path):
                if file == "structure.json":
                    f = open(file_path)
                    # Load the data as a dictionary.
                    data = json.load(f)
                    newdata = dictionary_unfold(data, {})
                    bigdictionary = dict_append(bigdictionary, newdata)
    out_file = open("total_structure.json", "w")
    json.dump(bigdictionary, out_file, indent="")
    return



def dict_append(dict1, dict2):
    for key in dict2:
        if dict1.get(key) is None:
            dict1[key] = dict2[key]
        else:
            if isinstance(dict2[key], list):
                dict1[key] = dict1[key] + dict2[key]
                dict1[key] = [*set(dict1[key])]
            else:
                print('ERROR not a list')
                return None
    return dict1

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
