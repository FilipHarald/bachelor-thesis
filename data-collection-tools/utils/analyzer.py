import math
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


def analyze_users(repo, dict, label):
    output = [repo['color'] + repo['name'], 'Unique users(' + str(len(dict)) + '): ' + str(dict)]
    plt.plot(get_distribution(dict), label=label)
    return '\n'.join(output)


def visualize_results(repos, datatype, contributors_data, filename):
    for repo in repos:
        analyze_users(repo, contributors_data[repo['name']][datatype + '_dict'], repo['name'])
    plotter.save('users (%)', datatype + ' (%)', filename)
