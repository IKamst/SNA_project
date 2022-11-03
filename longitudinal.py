from json import load, dump
import os
import datetime

EGO = '580341214098137089'
# input: fp = filepath of the .json file
# output: <class 'datetime.datetime'>
# reference: https: // www.geeksforgeeks.org / python - time - strptime - function /  #:~:text=The%20strptime()%20function%20in,according%20to%20the%20provided%20directives.
def scrap_time_from_file(fp):
    f = open(fp)
    data = load(f)
    datetime_obj = datetime.datetime.strptime(
        data["created_at"], '%a %b %d %H:%M:%S %z %Y')
    return datetime_obj, data["id"], 0


def create_timeline():
    wd = os.getcwd()
    base = wd + '/germanwings-crash-all-rnr-threads'
    times = []
    for rumourfolder in os.listdir(base):  # non-rumour and rumour
        path = base + '/' + rumourfolder
        if os.path.isdir(path):
            for directory_name in os.listdir(path):
                if directory_name == EGO:# directory_name = 580319983676313601
                    direc_path = path + '/' + directory_name
                    if os.path.isdir(direc_path):
                        # Loop over the files in that directory.
                        for file in os.listdir(direc_path + '/source-tweets'):
                            file_path = os.path.join(direc_path + '/source-tweets', file)
                            if file == (directory_name + '.json'):  # take only the source tweet file
                                times.append(scrap_time_from_file(file_path))
                        if os.path.exists(direc_path + '/reactions'):
                            for file in os.listdir(direc_path + '/reactions'):
                                file_path = os.path.join(direc_path + '/reactions', file)
                                if '_' not in file:  # only take tweets
                                    times.append(scrap_time_from_file(file_path))
    # sort it by time
    times.sort(key=lambda tup: tup[0])

    return times


def longitudinal_analysis():
    timeline = create_timeline()
    print(len(timeline))
    return
