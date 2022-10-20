import json
import os


# Reads the data from the structure.json file.
# TODO how to save the data to get the full correct structure?
# TODO input to save files for rumour and non-rumour?
def read_data_file():
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
                            # Prints the source tweet.
                            print(key)
                            # Prints the tweets linked to the source tweet and their inner structure.
                            # TODO how to get the structure if tweets continue further?
                            print(data[key])
                        # Closing file
                        f.close()
