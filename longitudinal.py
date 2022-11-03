from json import load, dump
from os import getcwd


def longitudinal_analysis(graph):
    test()
    return


def test():
    wd = getcwd()
    file_path = wd + '/germanwings-crash-all-rnr-threads/non-rumours/580319983676313601/reactions/580325737619685377.json'
    f = open(file_path)
    data = load(f)
    out_file = open(wd + "/testing_dictionary" + ".json", "w")
    dump(data, out_file, indent="")
    print(data["created_at"])
    return
