import json
import os


# Reads the data from the structure.json file.
def read_data_homophily(rumourboolpath, id_to_verified_dic):
    wd = os.getcwd()
    path = wd + '/germanwings-crash-all-rnr-threads/' + rumourboolpath
    # Loop over the directories of each tweet.
    for directory_name in os.listdir(path):
        direc_path = os.path.join(path, directory_name)
        if os.path.isdir(direc_path):
            id_to_verified_dic = determine_verified_dic(direc_path, id_to_verified_dic)
    print(id_to_verified_dic)
    return id_to_verified_dic


# Create a dictionary of user id with whether they are verified or not.
def determine_verified_dic(directory, tweet_to_id_dic):
    # Loop over reactions and source-tweets directories.
    for directory_name in os.listdir(directory):
        direc_path = os.path.join(directory, directory_name)
        if os.path.isdir(direc_path):
            # Loop over the tweets.
            for file in os.listdir(direc_path):
                if '_' not in file:
                    # Open the file and load the data.
                    file_path = os.path.join(direc_path, file)
                    f = open(file_path)
                    # Load the data as a dictionary.
                    data = json.load(f)
                    user = data["user"]
                    id_person = user["id"]
                    verified = user["verified"]
                    # Save whether the account is verified to the id.
                    tweet_to_id_dic[id_person] = verified
    return tweet_to_id_dic


# Small function to try out the code.
if __name__ == "__main__":
    id_to_verified_dic = {}
    id_to_verified_dic = read_data_homophily('non-rumours', id_to_verified_dic)
    id_to_verified_dic = read_data_homophily('rumours', id_to_verified_dic)
