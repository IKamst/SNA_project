import json
import os
import re

import networkx as nx

# Reads the data from the structure.json file.
def read_data_file(rumourboolpath):
    bigdictionary = {}
    wd = os.getcwd()
    path = wd + '/germanwings-crash-all-rnr-threads/' + rumourboolpath
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
                    #if directory_name == '580319983676313601':
                    newdata = replace_dictionary_values(newdata, direc_path, directory_name)
                    bigdictionary = dict_append(bigdictionary, newdata)
    out_file = open(wd + "/accounts/structure-" + rumourboolpath + ".json", "w")
    json.dump(bigdictionary, out_file, indent="")
    return bigdictionary


#name = directoary_name, dict = newdata, path = direc_path
# D:\bvjon\Documents\RUG\2022-2023 Msc Artificial Intelligence\Social Network Analysis\PHEME\SNA_project/germanwings-crash-all-rnr-threads/rumours\581293286268129280
def replace_dictionary_values(dict, path, name):
    for file in os.listdir(path + '/source-tweets'): #all files in the source_tweets folder
        if file == (name + '.json'):  # take only the source tweet file
            reactpath = path + '/reactions'
            if os.path.exists(reactpath):
                for reaction in os.listdir(reactpath):  #replace the values in the lists with their account names
                    # print(reaction)
                    # print(os.path.splitext(reaction)[0])
                    if '_' not in reaction:
                        f = open(reactpath + '\\' + reaction)
                        data = json.load(f)
                        #in  (the dict of the tweet), replace the value (list) by their account name

                        for k, i in dict.items(): #for every list in the dictionary
                            if len(dict[k]) != 0:
                                dict[k] = list(map(lambda x: x.replace(data["id_str"], str(data["user"]["id"])), dict[k]))

    # edit keys here
    # if two keys already
    # e.g. final dict: {'580355999825047552': [], '580390315485310976': [], '2280470022': ['63512083', '244436308']}
    newdict = {}
    for k, v in dict.items():
        #replace k
        # if k is the sourcetweet
        if k == name:
            f = open(path + '/source-tweets/' + name + ".json")
            f = json.load(f)
            z = str(f["user"]["id"])
            newdict[z] = dict[k]
        # if k is a reaction tweet
        else:
            for namefile in os.listdir(path + '/reactions'):
                if '_' not in namefile:
                    if k == os.path.splitext(namefile)[0]:
                        f = open(path+'/reactions/' + namefile)
                        f = json.load(f)
                        z = str(f["user"]["id"])
                        newdict[z] = dict[k]

    print("third final dict:", newdict)
    return newdict

def create_digraph(dict):
    G = nx.DiGraph(dict)
    # pos = nx.random_layout(G)
    # nx.draw_networkx(G, pos, with_labels=False, node_size=5)
    # plt.savefig("bigdictionarygraph.png")
    # plt.show()
    return G

# given a recursive dictionary of dictionaries,
def dictionary_unfold(data, big_dictionary):
    #base case
    if isinstance(data, list):
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
                print(data[key])
                big_dictionary[key] = big_dictionary[key] + list(data[key].keys()) # append the existing list
                big_dictionary[key] = [*set((big_dictionary[key]))]  # remove doubles
            big_dictionary = dictionary_unfold(data[key], big_dictionary)
        return big_dictionary


# appends two dictionaries of lists
# for both dict1 and dict2 of type with lists as value
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

# def determine_nodes_and_edges(graph, main_node, values):
#     # Prints the source tweet.
#     print(main_node)
#     graph.add_node(main_node)
#     # Prints the tweets linked to the source tweet and their inner structure.
#     print(values)
#     out = re.split(r"[:|,]", str(values))
#     print(out)
#     for elem in out:
#         print(elem)
#     return graph
