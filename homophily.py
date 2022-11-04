import json
import os
import re

import networkx as nx


# Reads the data from the structure.json file.
def read_data_homophily(rumourboolpath, id_to_verified_dic):
    wd = os.getcwd()
    path = wd + '/germanwings-crash-all-rnr-threads/' + rumourboolpath
    for directory_name in os.listdir(path):
        direc_path = os.path.join(path, directory_name)
        if os.path.isdir(direc_path):
            id_to_verified_dic = determine_verified_dic(direc_path, id_to_verified_dic)
    print(id_to_verified_dic)
    return id_to_verified_dic


def determine_verified_dic(directory, tweet_to_id_dic):
    for directory_name in os.listdir(directory):
        direc_path = os.path.join(directory, directory_name)
        if os.path.isdir(direc_path):
            for file in os.listdir(direc_path):
                if '_' not in file:
                    file_path = os.path.join(direc_path, file)
                    f = open(file_path)
                    # Load the data as a dictionary.
                    data = json.load(f)
                    user = data["user"]
                    id_person = user["id"]
                    verified = user["verified"]
                    tweet_to_id_dic[id_person] = verified
    return tweet_to_id_dic


if __name__ == "__main__":
    id_to_verified_dic = {}
    id_to_verified_dic = read_data_homophily('non-rumours', id_to_verified_dic)
    id_to_verified_dic = read_data_homophily('rumours', id_to_verified_dic)
