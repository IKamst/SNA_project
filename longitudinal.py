from json import load, dump
import os
import datetime

def test():
    wd = os.getcwd()
    file_path = wd + '/germanwings-crash-all-rnr-threads/non-rumours/580319983676313601/reactions/580325737619685377.json'
    f = open(file_path)
    data = load(f)
    out_file = open(wd + "/testing_dictionary" + ".json", "w")
    dump(data, out_file, indent="")
    print(data["created_at"])
    return


#input: fp = filepath of the .json file
#output: <class 'datetime.datetime'>
# reference: https: // www.geeksforgeeks.org / python - time - strptime - function /  #:~:text=The%20strptime()%20function%20in,according%20to%20the%20provided%20directives.
def scrap_time_from_file(fp):
    f = open(fp)
    data = load(f)
    datetime_obj = datetime.datetime.strptime(
        data["created_at"], '%a %b %d %H:%M:%S %z %Y')
    return datetime_obj

#https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
def sort_timeline(times):
    return times


def create_timeline():
    wd = os.getcwd()
    path = wd + '/germanwings-crash-all-rnr-threads' + '/non-rumours'
    times = []
    #'/germanwings-crash-all-rnr-threads/non-rumours/580319983676313601/reactions/580325737619685377.json')
    for directory_name in os.listdir(path): #directory_name = 580319983676313601
        #temporary: TODO remove this if-statement
        if directory_name == '580319983676313601':
            direc_path = path + '/'+ directory_name
            if os.path.isdir(direc_path):
                # Loop over the files in that directory.
                for file in os.listdir(direc_path + '/source-tweets'):
                    file_path = os.path.join(direc_path + '/source-tweets', file)
                    if file == (directory_name + '.json'): #if source
                        times.append(scrap_time_from_file(file_path))
            for file in os.listdir(direc_path + '/reactions'):
                    pass
                    # file_path = os.path.join(direc_path, file)
                    # if os.path.isfile(file_path):
                    #     if file == directory_name:
                    #         dt = scrap_time_from_file(file_path)
            pass
    print(times)
    times = sort_timeline(times)
    dt = scrap_time_from_file(wd + '/germanwings-crash-all-rnr-threads/non-rumours/580319983676313601/reactions/580325737619685377.json')
    return times


def longitudinal_analysis(graph):
    test()
    create_timeline()
    return

