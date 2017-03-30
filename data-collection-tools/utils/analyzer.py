import math
import os
from itertools import islice
import matplotlib.pyplot as plt

from utils import plotter


def get_distribution(dict):
    """"Returns an array for distribution of key and values in dict"""
    output = []
    tot_keys = len(dict)
    sum_values = sum(dict.values()) if sum(dict.values()) > 0 else 1
    sorted_values = sorted(dict.values(), reverse=True)
    for i in range(1, 101):
        n = math.ceil(tot_keys * i/100)
        output.append(sum(islice(sorted(sorted_values), n)) / sum_values*100)
    return output


def analyze_users(repo, dict, label, datatype):
    output = [repo['color'] + repo['name'], 'Unique users (' + datatype + '): ' + str(len(dict)),
              'Amount of ' + datatype + ': ' + str(sum(dict.values()))]
    plt.plot(get_distribution(dict), label=label)
    return '\n'.join(output)


def visualize_results(repos, datatype, contributors_data, filename):
    for repo in repos:
        data = analyze_users(repo, contributors_data[repo['name']][datatype + '_dict'], repo['name'], datatype)
        store(filename, repo, '.txt', data)
    plotter.save('users (%)', datatype + ' (%)', filename)


def analyze_repair_time(repos, datatype, repair_times_data, filename):
    for repo in repos:
        repair_array = sorted(repair_times_data[repo['name']][datatype + '_array'])
        data_dict = {'lowest': repair_array[0],
                     'highest': repair_array[len(repair_array) - 1],
                     'avarage': sum(repair_array) / len(repair_array),
                     'median': repair_array[int(len(repair_array) / 2)]}
        store(filename, repo, '.txt', data_dict)


def store(filename, repo, extension, data):
    file = os.path.join(os.path.dirname(__file__),
                        '../results/' + filename + '_' + repo['key'] + extension)
    with open(file, "w") as f:
        f.write(str(data))
