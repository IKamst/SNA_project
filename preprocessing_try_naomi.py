import json
import os
import re

import networkx as nx


# Reads the data from the structure.json file.
def read_data_file(rumourboolpath):
    bigdictionary = {}
    tweet_to_id_dic = {}
    wd = os.getcwd()
    path = wd + '/germanwings-crash-all-rnr-threads/' + rumourboolpath
    for directory_name in os.listdir(path):
        direc_path = os.path.join(path, directory_name)
        if os.path.isdir(direc_path):
            tweet_to_id_dic = determine_tweet_to_id_dic(direc_path, tweet_to_id_dic)
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
    out_file = open(wd + "/structures/structure-" + rumourboolpath + "TRY.json", "w")
    json.dump(bigdictionary, out_file, indent="")
    print(tweet_to_id_dic)
    return bigdictionary


def create_digraph(dict):
    G = nx.DiGraph(dict)
    # pos = nx.random_layout(G)
    # nx.draw_networkx(G, pos, with_labels=False, node_size=5)
    # plt.savefig("bigdictionarygraph.png")
    # plt.show()
    return G


# given a recursive dictionary of dictionaries,
def dictionary_unfold(data, big_dictionary):
    # base case
    if isinstance(data, list):
        return big_dictionary
    else:
        # loop over all the keys in data
        for key, value in data.items():
            # check if the key already exists
            if big_dictionary.get(key) is None:
                # only keep "first level entries" of the dict in the value
                if not isinstance(data[key], list):  # when data[key] = []
                    big_dictionary[key] = list(data[key].keys())
                else:
                    big_dictionary[key] = data[key]
            else:
                # if the key already exists, add to value
                big_dictionary[key] = big_dictionary[key] + list(data[key].keys())  # append the existing list
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


def determine_tweet_to_id_dic(directory, tweet_to_id_dic):
    for directory_name in os.listdir(directory):
        direc_path = os.path.join(directory, directory_name)
        if os.path.isdir(direc_path):
            for file in os.listdir(direc_path):
                if '_' not in file:
                    file_path = os.path.join(direc_path, file)
                    print(file_path)
                    f = open(file_path)
                    # Load the data as a dictionary.
                    data = json.load(f)
                    id_tweet = re.split(r"\.", str(file))
                    print(id_tweet[0])
                    print(str(data))
                    user = data["user"]
                    id_person = user["id"]
                    print(id_person)
                    tweet_to_id_dic[str(id_tweet[0])] = id_person
        print(tweet_to_id_dic)
    return tweet_to_id_dic


if __name__ == "__main__":
    read_data_file('non-rumours')
