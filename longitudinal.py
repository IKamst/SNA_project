from json import load, dump
import os
import datetime
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.cm import ScalarMappable

from preprocessing import dict_append
from matplotlib import pyplot as plt
import bisect

#the ID of the chosen source tweet
EGO = "580323498905702400"

# input: fp = filepath of the .json file
# output: <class 'datetime.datetime'>
#takes a filepath of a tweet and returns a datetime object when it was tweeted.
def scrap_time_from_file(fp):
    f = open(fp)
    data = load(f)
    datetime_obj = datetime.datetime.strptime(
        data["created_at"], '%a %b %d %H:%M:%S %z %Y')
    return datetime_obj


# just look at one source tweet
# pick some time intervals
# for every interval, plot how the graph looks at that second
# in the end, make 1 plot of x = time, y = total amount of reactions
def pick_source_folder():
    # find the path of the EGO
    pathfile = os.path.join(os.getcwd(), 'germanwings-crash-all-rnr-threads')
    pathfile = os.path.join(pathfile, 'non-rumours')
    EGOpath = os.path.join(pathfile, EGO)

    # make a list of all the times at which a reaction to the EGO was posted
    times = []
    if os.path.isdir(EGOpath): #loop over all tweets in the
        # Loop over the files in that directory.
        for file in os.listdir(EGOpath + '/source-tweets'):
            file_path = os.path.join(EGOpath + '/source-tweets', file)
            if file == (EGO + '.json'):  # take only the source tweet file and put the time inside.
                times.append(scrap_time_from_file(file_path))
        if os.path.exists(EGOpath + '/reactions'):
            for file in os.listdir(EGOpath + '/reactions'):
                file_path = os.path.join(EGOpath + '/reactions', file)
                if '_' not in file:  # only take tweets
                    times.append(scrap_time_from_file(file_path))
    #sort the times
    times.sort()
    print(times[0]) #first tweet (EGO)
    print(times[-1]) #last tweet
    print(len(times))
    i=0
    while i < len(times):
        times[i].replace(tzinfo=None)
        i=i+1
    print(datetime.datetime(2015, 3, 26, 0, 0, 0))
    boundary = bisect.bisect_left(times, datetime.datetime(2015, 3, 26, 0, 0, 0).replace(tzinfo=datetime.timezone.utc))
    print(boundary)

    # make dict per interval
    interval_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
    interval = [datetime.time(hour=11, minute=1, second=17),
                datetime.time(hour=11, minute=6, second=18),
                datetime.time(hour=11, minute=16, second=18),
                datetime.time(hour=11, minute=31, second=18),
                datetime.time(hour=12, minute=1, second=18),
                datetime.time(hour=23, minute=59, second=59)
                ]

    G_nodes = []
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
                        interval_dict[i][str(rdict["in_reply_to_status_id"])].append(os.path.splitext(r)[0])
                    else:
                        interval_dict[i][str(rdict["in_reply_to_status_id"])] = [os.path.splitext(r)[0]]
        if i > 0:
            interval_dict[i] = dict_append(interval_dict[i], interval_dict[i-1])
        G = nx.DiGraph(interval_dict[i])

        #assign color red to new nodes
        colormap = []
        G_nodes.append(G.nodes)
        if i > 0:
            diff = set(G_nodes[i]) - set(G_nodes[i-1])
            for node in G:
                if node in diff:
                    colormap.append('red')
                else:
                    colormap.append('#1f78b4')
        if i == 0:
            colormap = '#1f78b4'
        G = G.reverse()
        pos = nx.kamada_kawai_layout(G)
        nx.draw_networkx(G, pos=pos, with_labels=False, node_size=150, node_color=colormap)
        plt.title('Graph at timestamp ' + str(i), fontsize = 18)
        plt.savefig("longitudinal_" + str(i) + ".png", bbox_inches="tight")
        plt.show()
                    # if within the interval, let it stay in the structure
                # use "in_reply_to_status_id"
    print(interval_dict)
    return interval_dict


def graph_from_interval_dict(id):
    colormap = []
    graph0 = nx.DiGraph(id[0])
    graph0 = graph0.nodes
    graph1 = nx.DiGraph(id[1])
    graph1 = graph1.nodes
    graph2 = nx.DiGraph(id[2])
    graph2 = graph2.nodes
    graph3 = nx.DiGraph(id[3])
    graph3 = graph3.nodes
    G = nx.DiGraph(id[4])
    graph4 = G.nodes
    for n in G.nodes:
        if n in graph0:
            colormap.append('#dce4a8')
        if n in graph1 and n not in graph0:
            colormap.append('#94c099')
        if n in graph2 and n not in graph1:
            colormap.append('#5c998c')
        if n in graph3 and n not in graph2:
            colormap.append('#3a7077')
        if n in graph4 and n not in graph3:
            colormap.append('#2a4858')
    G = G.reverse()
    pos = nx.kamada_kawai_layout(G)
    plt.figure()
    nx.draw_networkx(G, pos=pos, with_labels=False, node_size=150, node_color=colormap)
    plt.title('Longitudinal Graph', fontsize = 18)
    # ax = plt.subplot()
    # im = ax.imshow(np.arange(100).reshape((10, 10)))
    cm = LinearSegmentedColormap.from_list('defcol', ['#dce4a8', '#2a4858'])
    cb = plt.colorbar(ScalarMappable(cmap=cm, norm=plt.Normalize(0, 5 - 1)), ticks=range(5))
    cb.set_label(label='Timestamp', fontsize = 15)
    plt.savefig("longitudinal.png", bbox_inches="tight")
    plt.show()
    return


def longitudinal_analysis():
    id = pick_source_folder()
    #graph_from_interval_dict(id)
    return
