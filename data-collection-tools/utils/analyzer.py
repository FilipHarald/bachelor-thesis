import math
import os
from itertools import islice
import matplotlib.pyplot as plt
import numpy as np

from utils import plotter


def get_distribution(dict):
    """"Returns an array for distribution of key and values in dict"""
    output = {}
    tot_keys = len(dict)
    sum_values = sum(dict.values()) if sum(dict.values()) > 0 else 1
    sorted_values = sorted(dict.values())
    output['y'] = np.linspace(0, sum_values, num=100)
    output['x'] = []
    for i in range(0, 100):
        n = math.ceil(tot_keys * i/100)
        output['x'].append(sum(islice(sorted(sorted_values), n)) / sum_values*100)
    print(output['x'])
    return output


def analyze_users(repo, dict, label, datatype):
    output = [repo['color'] + repo['name'], 'Unique users (' + datatype + '): ' + str(len(dict)),
              'Amount of ' + datatype + ': ' + str(sum(dict.values()))]
    dist_data = get_distribution(dict)
    plt.plot(dist_data['y'], dist_data['x'], label=label)
    return '\n'.join(output)


def visualize_results(repos, datatype, contributors_data, filename, unit=None, x_axis=None):
    for repo in repos:
        data = analyze_users(repo, contributors_data[repo['name']][datatype + '_dict'], repo['name'], datatype)
        store(filename, repo, '.txt', data)
    datatype = x_axis if x_axis else datatype
    datatype = datatype if not unit else datatype + ' (' + unit + ')'
    plotter.save(datatype, 'users (%)', filename + '_dist')


def analyze_repair_time(repos, datatype, repair_times_data, filename):
    for repo in repos:
        repair_array = sorted(repair_times_data[repo['name']][datatype + '_array'])
        data_dict = {'lowest': repair_array[0],
                     'highest': repair_array[len(repair_array) - 1],
                     'avarage': sum(repair_array) / len(repair_array),
                     'median': repair_array[int(len(repair_array) / 2)],
                     'amount': len(repair_array)}
        store(filename, repo, '.txt', data_dict)


def store(filename, repo, extension, data):
    file = os.path.join(os.path.dirname(__file__),
                        '../results/' + filename + '_' + repo['key'] + extension)
    with open(file, "w") as f:
        f.write(str(data))
