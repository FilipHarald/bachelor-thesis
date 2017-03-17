import math
from itertools import islice


def get_distribution(unique_dict):
    """"Returns an array for distribution of key and values in dict"""
    output = []
    tot_keys = len(unique_dict)
    sum_values = sum(unique_dict.values())
    sorted_values = sorted(unique_dict.values(), reverse=True)
    for i in range(1, 101):
        n = math.ceil(tot_keys * i/100)
        output.append(sum(islice(sorted(sorted_values), n)) / sum_values*100)
    return output
