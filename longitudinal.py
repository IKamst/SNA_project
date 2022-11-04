from json import load, dump
import os
import datetime
import networkx as nx
from matplotlib import pyplot as plt

EGO = "580323498905702400"


# input: fp = filepath of the .json file
# output: <class 'datetime.datetime'>
def scrap_time_from_file(fp):
    f = open(fp)
    data = load(f)
    datetime_obj = datetime.datetime.strptime(
        data["created_at"], '%a %b %d %H:%M:%S %z %Y')
    return datetime_obj


# just look at one source tweet
# pick some time intervals, lets say 1 hour and take 6 hours
# for every interval, plot how the graph looks at that second
# in the end, make 1 plot of x = time, y = total amount of reactions
#returns a
def pick_source_folder():
    # find the path of the EGO
    pathfile = os.path.join(os.getcwd(), 'germanwings-crash-all-rnr-threads')
    pathfile = os.path.join(pathfile, 'non-rumours')
    EGOpath = os.path.join(pathfile, EGO)

    # make a list of all the times at which a reaction to the EGO was posted
    times = []
    if os.path.isdir(EGOpath):
        # Loop over the files in that directory.
        for file in os.listdir(EGOpath + '/source-tweets'):
            file_path = os.path.join(EGOpath + '/source-tweets', file)
            if file == (EGO + '.json'):  # take only the source tweet file
                times.append(scrap_time_from_file(file_path))
        if os.path.exists(EGOpath + '/reactions'):
            for file in os.listdir(EGOpath + '/reactions'):
                file_path = os.path.join(EGOpath + '/reactions', file)
                if '_' not in file:  # only take tweets
                    times.append(scrap_time_from_file(file_path))
    # sort these times
    # times.sort(key=lambda tup: tup[0])
    times.sort()
    # print(times[0]) #first tweet (EGO)
    # print(times[-1]) #last tweet

    # print only the times (all posted on the same date)
    # i=0
    # while i < len(times):
    #     t = times[i][0].time()
    #     if t > datetime.time(hour=12, minute=1, second=18):
    #
    #         print(t)
    #     i=i+1

    # make dict per interval
    interval_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    interval = [datetime.time(hour=10, minute=0, second=0),
                datetime.time(hour=11, minute=1, second=18),
                datetime.time(hour=11, minute=6, second=18),
                datetime.time(hour=11, minute=16, second=18),
                datetime.time(hour=11, minute=31, second=18),
                datetime.time(hour=12, minute=1, second=18),
                datetime.time(hour=23, minute=59, second=59)
                ]
    print(interval)

    for i in range(5):
        for r in os.listdir(EGOpath + '/reactions'):
            r_path = os.path.join(EGOpath + '/reactions', r)
            if '_' not in r:  # loop through the reactions
                # find the time of the file
                rf = open(r_path)
                rdict = load(rf)
                t = scrap_time_from_file(r_path).time()
                if t > interval[i] and t < interval[i + 1]:
                    i_dict = interval_dict[i]
                    # check if this key already exists in i_dict
                    if str(rdict["in_reply_to_status_id"]) in i_dict.keys():
                        i_dict[str(rdict["in_reply_to_status_id"])].append(os.path.splitext(r)[0])
                    else:
                        i_dict[str(rdict["in_reply_to_status_id"])] = [os.path.splitext(r)[0]]
                    # if within the interval, let it stay in the structure
                # use "in_reply_to_status_id"
    print(interval_dict)
    return interval_dict

#id is dict with graph-dictionary per interval
def graph_from_interval_dict(id):
    for v in id.values():
        print(v)
        G = nx.DiGraph(v)
        G = G.reverse()
        nx.draw_networkx(G, pos=nx.random_layout(G), with_labels=False, node_size=100)
        #plt.show()


def create_timeline():
    wd = os.getcwd()
    base = wd + '/germanwings-crash-all-rnr-threads'
    times = []
    for rumourfolder in os.listdir(base):  # non-rumour and rumour
        path = base + '/' + rumourfolder
        if os.path.isdir(path):
            for directory_name in os.listdir(path):
                # if directory_name == EGO:# directory_name = 580319983676313601
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
    print(len(times))
    print(times[0])
    return times


def longitudinal_analysis():
    # timeline = create_timeline()
    # print(len(timeline))
    id = pick_source_folder()
    graph_from_interval_dict(id)
    return
